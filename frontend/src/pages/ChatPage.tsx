import {
  useCallback,
  useEffect,
  useLayoutEffect,
  useMemo,
  useRef,
  useState,
  type FormEvent,
  type KeyboardEvent,
} from "react";
import { useSearchParams } from "react-router-dom";
import { ApiError } from "../api/client";
import {
  clearChatHistory,
  getChatHistory,
  sendChatMessage,
} from "../api/chat";
import type { ChatHistoryItem } from "../api/types";
import { ErrorState } from "../components/ErrorState";
import { Spinner } from "../components/Spinner";
import { useChatSession } from "../hooks/useChatSession";
import { formatDateTime } from "../lib/format";

interface PendingState {
  loading: boolean;
  error?: string;
}

const SUGGESTIONS = [
  "Recomiendame zapatos Nike para correr largas distancias",
  "Que opciones tienen en talla 42?",
  "Necesito un zapato formal para una boda",
  "Cual es el modelo casual mas vendido bajo $100?",
];

const INPUT_MAX_LENGTH = 2000;

export function ChatPage() {
  const { sessionId, resetSession } = useChatSession();
  const [searchParams, setSearchParams] = useSearchParams();
  const [messages, setMessages] = useState<ChatHistoryItem[]>([]);
  // Prefill the input from `?ref=...` when arriving from a product page.
  const [input, setInput] = useState<string>(() => {
    const ref =
      typeof window === "undefined"
        ? null
        : new URLSearchParams(window.location.search).get("ref");
    return ref ? `Cuentame mas sobre ${ref}.` : "";
  });
  const [historyLoading, setHistoryLoading] = useState(true);
  const [historyError, setHistoryError] = useState<string | undefined>();
  const [pending, setPending] = useState<PendingState>({ loading: false });
  const [confirmingClear, setConfirmingClear] = useState(false);
  const listRef = useRef<HTMLDivElement | null>(null);
  const textareaRef = useRef<HTMLTextAreaElement | null>(null);

  // Clean up the prefill query param so it doesn't stick on reload.
  useEffect(() => {
    if (!searchParams.get("ref")) return;
    setSearchParams(
      (prev) => {
        const next = new URLSearchParams(prev);
        next.delete("ref");
        return next;
      },
      { replace: true },
    );
  }, [searchParams, setSearchParams]);

  // Initial history load (no sync setState in effect body — only inside callbacks).
  useEffect(() => {
    const controller = new AbortController();
    let cancelled = false;

    getChatHistory(sessionId, 50, controller.signal)
      .then((history) => {
        if (cancelled) return;
        setMessages(history);
        setHistoryError(undefined);
        setHistoryLoading(false);
      })
      .catch((error: unknown) => {
        if (cancelled) return;
        if (error instanceof DOMException && error.name === "AbortError") return;
        setHistoryError(
          error instanceof Error ? error.message : "Error al cargar el historial",
        );
        setHistoryLoading(false);
      });

    return () => {
      cancelled = true;
      controller.abort();
    };
  }, [sessionId]);

  const reloadHistory = useCallback(() => {
    setHistoryLoading(true);
    setHistoryError(undefined);
    getChatHistory(sessionId, 50)
      .then((history) => {
        setMessages(history);
        setHistoryLoading(false);
      })
      .catch((error: unknown) => {
        setHistoryError(
          error instanceof Error ? error.message : "Error al cargar el historial",
        );
        setHistoryLoading(false);
      });
  }, [sessionId]);

  // Auto-scroll to bottom on new messages or while assistant types.
  useLayoutEffect(() => {
    const node = listRef.current;
    if (!node) return;
    node.scrollTo({ top: node.scrollHeight, behavior: "smooth" });
  }, [messages.length, pending.loading]);

  // Auto-grow textarea up to a max height.
  useLayoutEffect(() => {
    const ta = textareaRef.current;
    if (!ta) return;
    ta.style.height = "auto";
    ta.style.height = `${Math.min(ta.scrollHeight, 180)}px`;
  }, [input]);

  const trimmedInput = input.trim();
  const canSend = trimmedInput.length > 0 && !pending.loading;

  const submit = useCallback(async () => {
    if (!canSend) return;
    const userMessage = trimmedInput;
    const optimisticId = -Date.now();

    setMessages((prev) => [
      ...prev,
      {
        id: optimisticId,
        role: "user",
        message: userMessage,
        timestamp: new Date().toISOString(),
      },
    ]);
    setInput("");
    setPending({ loading: true });

    try {
      const response = await sendChatMessage({
        session_id: sessionId,
        message: userMessage,
      });
      setMessages((prev) => [
        ...prev.filter((msg) => msg.id !== optimisticId),
        {
          id: optimisticId - 1,
          role: "user",
          message: response.user_message,
          timestamp: response.timestamp,
        },
        {
          id: optimisticId - 2,
          role: "assistant",
          message: response.assistant_message,
          timestamp: response.timestamp,
        },
      ]);
      setPending({ loading: false });
    } catch (error) {
      const detail =
        error instanceof ApiError
          ? error.message
          : error instanceof Error
            ? error.message
            : "Error al enviar el mensaje";
      setMessages((prev) => prev.filter((msg) => msg.id !== optimisticId));
      setInput(userMessage);
      setPending({ loading: false, error: detail });
    }
  }, [canSend, sessionId, trimmedInput]);

  const handleSubmit = useCallback(
    (event: FormEvent<HTMLFormElement>) => {
      event.preventDefault();
      void submit();
    },
    [submit],
  );

  const handleKeyDown = useCallback(
    (event: KeyboardEvent<HTMLTextAreaElement>) => {
      if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        void submit();
      }
    },
    [submit],
  );

  const handleResetSession = useCallback(() => {
    resetSession();
    setMessages([]);
    setPending({ loading: false });
    setConfirmingClear(false);
  }, [resetSession]);

  const handleClearHistory = useCallback(async () => {
    try {
      await clearChatHistory(sessionId);
      setMessages([]);
      setPending({ loading: false });
    } catch (error) {
      setPending({
        loading: false,
        error:
          error instanceof Error ? error.message : "No se pudo limpiar el historial",
      });
    } finally {
      setConfirmingClear(false);
    }
  }, [sessionId]);

  const handleSuggestion = useCallback((suggestion: string) => {
    setInput(suggestion);
    textareaRef.current?.focus();
  }, []);

  const isEmpty = !historyLoading && messages.length === 0 && !pending.loading;
  const sessionShortId = useMemo(() => sessionId.slice(0, 8), [sessionId]);

  return (
    <section className="flex min-h-[72vh] flex-col gap-6">
      <header className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div className="space-y-2">
          <p className="eyebrow">Asistente</p>
          <h1 className="font-display text-display-xl text-ink">
            Conversa con un experto del catalogo.
          </h1>
          <p className="max-w-prose text-base leading-relaxed text-muted">
            Cuentale tu uso, marca preferida o talla. Responde con opciones reales
            del inventario.
          </p>
        </div>
        <dl className="flex gap-x-6 gap-y-1 text-sm sm:flex-col sm:gap-x-0 sm:text-right">
          <div>
            <dt className="eyebrow">Sesion</dt>
            <dd className="font-mono text-ink">{sessionShortId}…</dd>
          </div>
          <div>
            <dt className="eyebrow">Mensajes</dt>
            <dd className="font-mono text-ink">
              {String(messages.length).padStart(2, "0")}
            </dd>
          </div>
        </dl>
      </header>

      <div className="flex flex-wrap items-center justify-between gap-2 border-y border-line py-2">
        <div className="flex items-center gap-2 text-xs text-muted">
          <StatusDot active={!pending.loading} />
          <span>
            {pending.loading
              ? "El asistente esta escribiendo…"
              : "Listo para conversar"}
          </span>
        </div>
        <div className="flex items-center gap-1">
          {confirmingClear ? (
            <>
              <span className="text-xs text-muted">Eliminar historial?</span>
              <button
                type="button"
                className="btn-ghost h-9 px-3 text-xs sm:h-8 sm:px-2"
                onClick={() => setConfirmingClear(false)}
              >
                Cancelar
              </button>
              <button
                type="button"
                className="btn-accent h-9 px-3 text-xs sm:h-8"
                onClick={() => void handleClearHistory()}
              >
                Confirmar
              </button>
            </>
          ) : (
            <>
              <button
                type="button"
                className="btn-ghost h-9 px-3 text-xs sm:h-8 sm:px-2"
                onClick={() => setConfirmingClear(true)}
                disabled={messages.length === 0 || pending.loading}
              >
                Limpiar historial
              </button>
              <button
                type="button"
                className="btn-ghost h-9 px-3 text-xs sm:h-8 sm:px-2"
                onClick={handleResetSession}
              >
                Nueva sesion
              </button>
            </>
          )}
        </div>
      </div>

      <div
        ref={listRef}
        className="scroll-soft min-h-[40vh] flex-1 space-y-5 overflow-y-auto pb-2 pr-1"
        aria-live="polite"
        aria-label="Conversacion"
      >
        {historyLoading ? (
          <div className="py-8">
            <Spinner label="Cargando conversacion" />
          </div>
        ) : historyError ? (
          <ErrorState message={historyError} onRetry={reloadHistory} />
        ) : isEmpty ? (
          <EmptyConversation onPick={handleSuggestion} />
        ) : (
          <>
            {messages.map((message, index) => (
              <MessageBubble
                key={message.id}
                message={message}
                isLast={index === messages.length - 1}
              />
            ))}
            {pending.loading ? <TypingIndicator /> : null}
          </>
        )}
      </div>

      {pending.error ? (
        <ErrorState
          title="No se pudo enviar el mensaje"
          message={pending.error}
          onRetry={() => void submit()}
        />
      ) : null}

      <form onSubmit={handleSubmit} className="space-y-2">
        <div className="panel flex items-end gap-2 p-2">
          <label htmlFor="chat-input" className="sr-only">
            Mensaje para el asistente
          </label>
          <textarea
            ref={textareaRef}
            id="chat-input"
            className="flex-1 resize-none bg-transparent px-3 py-2 text-sm text-ink placeholder:text-muted focus:outline-none"
            rows={1}
            placeholder="Escribe tu pregunta… (Enter para enviar, Shift+Enter para nueva linea)"
            value={input}
            onChange={(event) => setInput(event.target.value)}
            onKeyDown={handleKeyDown}
            disabled={pending.loading}
            maxLength={INPUT_MAX_LENGTH}
          />
          <button type="submit" className="btn-primary self-stretch" disabled={!canSend}>
            {pending.loading ? "Enviando" : "Enviar"}
            <ArrowUp />
          </button>
        </div>
        <div className="flex items-center justify-between text-[11px] text-muted">
          <span>
            {input.length} / {INPUT_MAX_LENGTH}
          </span>
          <span>Powered by Google Gemini AI</span>
        </div>
      </form>
    </section>
  );
}

interface StatusDotProps {
  active: boolean;
}
function StatusDot({ active }: StatusDotProps) {
  return (
    <span
      aria-hidden="true"
      className="relative inline-flex h-2 w-2"
    >
      {active ? (
        <span
          className="absolute inset-0 animate-ping rounded-full opacity-50"
          style={{ background: "var(--accent)" }}
        />
      ) : null}
      <span
        className="relative inline-block h-2 w-2 rounded-full"
        style={{ background: active ? "var(--accent)" : "var(--muted)" }}
      />
    </span>
  );
}

interface MessageBubbleProps {
  message: ChatHistoryItem;
  isLast: boolean;
}

function MessageBubble({ message, isLast }: MessageBubbleProps) {
  const isUser = message.role === "user";
  const stamp = formatDateTime(message.timestamp);

  if (isUser) {
    return (
      <div className="flex flex-col items-end gap-1.5">
        <div
          className="max-w-[85%] rounded-xl px-4 py-3 text-sm text-[color:var(--accent-ink)] sm:max-w-2xl"
          style={{ background: "var(--ink)" }}
        >
          <p className="whitespace-pre-wrap leading-relaxed">{message.message}</p>
        </div>
        <p className="font-mono text-[10px] uppercase tracking-eyebrow text-muted">
          Tu · {stamp}
        </p>
      </div>
    );
  }

  return (
    <div className="flex flex-col items-start gap-1.5">
      <div className="flex items-baseline gap-2">
        <span
          className="grid h-6 w-6 place-items-center rounded-full text-[10px] font-bold uppercase tracking-eyebrow text-[color:var(--accent-ink)]"
          style={{ background: "var(--accent)" }}
          aria-hidden="true"
        >
          IA
        </span>
        <span className="eyebrow">Asistente</span>
        {isLast ? (
          <span className="font-mono text-[10px] uppercase tracking-eyebrow text-muted">
            ultima respuesta
          </span>
        ) : null}
      </div>
      <div className="max-w-prose pl-8 text-sm leading-relaxed text-ink">
        <p className="whitespace-pre-wrap">{message.message}</p>
      </div>
      <p className="pl-8 font-mono text-[10px] uppercase tracking-eyebrow text-muted">
        {stamp}
      </p>
    </div>
  );
}

function TypingIndicator() {
  return (
    <div className="flex items-baseline gap-2">
      <span
        className="grid h-6 w-6 place-items-center rounded-full text-[10px] font-bold uppercase tracking-eyebrow text-[color:var(--accent-ink)]"
        style={{ background: "var(--accent)" }}
        aria-hidden="true"
      >
        IA
      </span>
      <span className="eyebrow">Asistente esta escribiendo</span>
      <span className="ml-1 inline-flex items-end gap-1">
        <Dot delay={0} />
        <Dot delay={120} />
        <Dot delay={240} />
      </span>
    </div>
  );
}

function Dot({ delay }: { delay: number }) {
  return (
    <span
      className="inline-block h-1.5 w-1.5 animate-bounce rounded-full"
      style={{ background: "var(--ink)", animationDelay: `${delay}ms` }}
    />
  );
}

function EmptyConversation({ onPick }: { onPick: (text: string) => void }) {
  return (
    <div className="grid gap-6 sm:grid-cols-[minmax(0,1fr)_auto] sm:items-start">
      <div className="space-y-3">
        <p className="eyebrow">Empieza por aqui</p>
        <p className="font-display text-display-md text-ink">
          Que zapato estas buscando?
        </p>
        <p className="max-w-prose text-sm text-muted">
          El asistente conoce el inventario completo: marcas, tallas, precios y
          stock. Puede comparar modelos y sugerir alternativas si algo esta agotado.
        </p>
      </div>

      <ul className="grid gap-2 sm:max-w-sm">
        {SUGGESTIONS.map((suggestion, index) => (
          <li key={suggestion}>
            <button
              type="button"
              onClick={() => onPick(suggestion)}
              className="group flex w-full items-baseline gap-3 rounded-lg p-3 text-left transition-colors hover:bg-surface-sunken"
            >
              <span className="font-mono text-[10px] uppercase tracking-eyebrow text-muted">
                {String(index + 1).padStart(2, "0")}
              </span>
              <span className="text-sm text-ink">{suggestion}</span>
              <ArrowRight className="ml-auto h-3.5 w-3.5 shrink-0 text-muted transition-colors group-hover:text-ink" />
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

function ArrowRight({ className = "" }: { className?: string }) {
  return (
    <svg
      aria-hidden="true"
      viewBox="0 0 16 16"
      className={className}
      fill="none"
      stroke="currentColor"
      strokeWidth="1.6"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M3 8h10M9 4l4 4-4 4" />
    </svg>
  );
}

function ArrowUp() {
  return (
    <svg
      aria-hidden="true"
      viewBox="0 0 16 16"
      className="h-3.5 w-3.5"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M8 13V3M3 8l5-5 5 5" />
    </svg>
  );
}

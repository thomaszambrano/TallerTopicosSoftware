import { useCallback, useEffect, useState } from "react";

const STORAGE_KEY = "shoeStore.chatSessionId";

function generateSessionId(): string {
  if (typeof crypto !== "undefined" && "randomUUID" in crypto) {
    return crypto.randomUUID();
  }
  return `session-${Date.now()}-${Math.random().toString(36).slice(2, 10)}`;
}

function readStoredSession(): string {
  if (typeof window === "undefined") {
    return generateSessionId();
  }
  try {
    const existing = window.localStorage.getItem(STORAGE_KEY);
    if (existing) return existing;
  } catch {
    /* localStorage may be unavailable (private mode, etc.) */
  }

  const created = generateSessionId();
  try {
    window.localStorage.setItem(STORAGE_KEY, created);
  } catch {
    /* ignore */
  }
  return created;
}

export function useChatSession(): {
  sessionId: string;
  resetSession: () => string;
} {
  const [sessionId, setSessionId] = useState<string>(() => readStoredSession());

  useEffect(() => {
    try {
      window.localStorage.setItem(STORAGE_KEY, sessionId);
    } catch {
      /* ignore */
    }
  }, [sessionId]);

  const resetSession = useCallback(() => {
    const next = generateSessionId();
    setSessionId(next);
    return next;
  }, []);

  return { sessionId, resetSession };
}

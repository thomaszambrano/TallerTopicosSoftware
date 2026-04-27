import { apiRequest } from "./client";
import type {
  ChatHistoryItem,
  ChatMessageRequest,
  ChatMessageResponse,
} from "./types";

export function sendChatMessage(
  payload: ChatMessageRequest,
  signal?: AbortSignal,
): Promise<ChatMessageResponse> {
  return apiRequest<ChatMessageResponse>("/chat", {
    method: "POST",
    body: payload,
    signal,
  });
}

export function getChatHistory(
  sessionId: string,
  limit = 20,
  signal?: AbortSignal,
): Promise<ChatHistoryItem[]> {
  return apiRequest<ChatHistoryItem[]>(
    `/chat/history/${encodeURIComponent(sessionId)}`,
    {
      query: { limit },
      signal,
    },
  );
}

export function clearChatHistory(
  sessionId: string,
): Promise<{ message: string; mensajes_eliminados: number }> {
  return apiRequest(
    `/chat/history/${encodeURIComponent(sessionId)}`,
    { method: "DELETE" },
  );
}

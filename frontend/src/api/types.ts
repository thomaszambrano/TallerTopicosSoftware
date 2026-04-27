export interface Product {
  id: number;
  name: string;
  brand: string;
  category: string;
  size: string;
  color: string;
  price: number;
  stock: number;
  description: string;
}

export interface ChatMessageRequest {
  session_id: string;
  message: string;
}

export interface ChatMessageResponse {
  session_id: string;
  user_message: string;
  assistant_message: string;
  timestamp: string;
}

export interface ChatHistoryItem {
  id: number;
  role: "user" | "assistant";
  message: string;
  timestamp: string;
}

export interface ProductFilters {
  brand?: string;
  category?: string;
}

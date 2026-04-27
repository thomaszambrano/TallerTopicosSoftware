import { apiRequest } from "./client";
import type { Product, ProductFilters } from "./types";

export function getProducts(
  filters: ProductFilters = {},
  signal?: AbortSignal,
): Promise<Product[]> {
  return apiRequest<Product[]>("/products", {
    query: {
      brand: filters.brand,
      category: filters.category,
    },
    signal,
  });
}

export function getProductById(
  id: number,
  signal?: AbortSignal,
): Promise<Product> {
  return apiRequest<Product>(`/products/${id}`, { signal });
}

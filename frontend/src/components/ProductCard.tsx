import { Link } from "react-router-dom";
import type { Product } from "../api/types";
import { formatCurrency } from "../lib/format";
import { ProductMark } from "./ProductMark";

interface ProductCardProps {
  product: Product;
  variant?: "default" | "feature";
  index?: number;
}

/**
 * Editorial-style product card.
 * Two variants:
 *   - "default": vertical card for the main grid
 *   - "feature": large horizontal hero used at the top of the catalog
 */
export function ProductCard({
  product,
  variant = "default",
  index,
}: ProductCardProps) {
  const inStock = product.stock > 0;

  if (variant === "feature") {
    return (
      <Link
        to={`/products/${product.id}`}
        className="group grid grid-cols-1 gap-6 rounded-xl border border-line bg-surface-raised p-5 transition-shadow duration-200 hover:shadow-edge sm:grid-cols-[minmax(0,1.1fr)_minmax(0,1fr)] sm:gap-8 sm:p-6"
      >
        <ProductMark
          product={product}
          size="lg"
          className="aspect-[5/4] w-full group-hover:scale-[1.01]"
        />
        <div className="flex flex-col justify-between gap-6">
          <div className="space-y-2">
            <p className="eyebrow">Pieza destacada · {product.brand}</p>
            <h2 className="font-display text-display-lg text-ink">{product.name}</h2>
            <p className="max-w-prose text-sm leading-relaxed text-muted">
              {product.description}
            </p>
          </div>
          <div className="flex flex-wrap items-end justify-between gap-3">
            <div className="flex flex-wrap gap-1.5">
              <span className="chip">{product.category}</span>
              <span className="chip">Talla {product.size}</span>
              <span className="chip">{product.color}</span>
            </div>
            <div className="text-right">
              <p className="eyebrow">Precio</p>
              <p className="font-display text-2xl font-semibold tracking-tightish">
                {formatCurrency(product.price)}
              </p>
            </div>
          </div>
        </div>
      </Link>
    );
  }

  return (
    <Link
      to={`/products/${product.id}`}
      className="group flex flex-col gap-3"
      aria-label={`${product.brand} ${product.name}`}
    >
      <div className="relative">
        <ProductMark
          product={product}
          size="md"
          className="aspect-[4/3] w-full transition-transform duration-300 ease-out group-hover:scale-[1.015]"
        />
        <span
          className={[
            "absolute right-3 top-3 chip text-[10px] uppercase tracking-eyebrow",
            inStock ? "" : "opacity-80",
          ].join(" ")}
          style={
            inStock
              ? undefined
              : { background: "var(--surface)", color: "var(--muted)" }
          }
        >
          {inStock ? `${product.stock} disp.` : "Agotado"}
        </span>
        {typeof index === "number" ? (
          <span className="absolute left-3 top-3 font-mono text-[10px] uppercase tracking-eyebrow text-ink">
            {String(index + 1).padStart(2, "0")}
          </span>
        ) : null}
      </div>

      <div className="flex items-baseline justify-between gap-3">
        <div className="min-w-0">
          <p className="eyebrow">{product.brand}</p>
          <h3 className="truncate font-display text-base font-medium text-ink">
            {product.name}
          </h3>
        </div>
        <p className="shrink-0 font-medium text-ink">
          {formatCurrency(product.price)}
        </p>
      </div>

      <div className="flex flex-wrap gap-1.5 text-xs text-muted">
        <span>{product.category}</span>
        <span aria-hidden="true">·</span>
        <span>Talla {product.size}</span>
        <span aria-hidden="true">·</span>
        <span>{product.color}</span>
      </div>
    </Link>
  );
}

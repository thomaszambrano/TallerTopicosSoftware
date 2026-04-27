import type { Product } from "../api/types";

interface ProductMarkProps {
  product: Product;
  size?: "sm" | "md" | "lg";
  className?: string;
}

const SIZES: Record<NonNullable<ProductMarkProps["size"]>, string> = {
  sm: "h-12 w-20",
  md: "h-20 w-32",
  lg: "h-32 w-48",
};

/**
 * Visual product placeholder with the product initials and a subtle shoe glyph.
 * Avoids the AI-tell of repeating a uniform stock illustration on every card.
 * The hue of the gradient is derived from the product id so each item feels distinct.
 */
export function ProductMark({ product, size = "md", className = "" }: ProductMarkProps) {
  const initials = (product.brand || product.name)
    .split(/\s+/)
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0]?.toUpperCase() ?? "")
    .join("");

  const hue = ((product.id ?? 0) * 47) % 360;
  const accentBg = `oklch(94% 0.04 ${hue})`;
  const inkBg = `oklch(82% 0.06 ${hue})`;

  return (
    <div
      className={[
        "relative isolate overflow-hidden rounded-lg",
        "transition-transform duration-300 ease-out",
        className,
      ].join(" ")}
      style={{ background: accentBg }}
      aria-hidden="true"
    >
      <span
        className="absolute -bottom-6 -right-6 h-32 w-32 rounded-full opacity-70 blur-2xl"
        style={{ background: inkBg }}
      />
      <div className="relative flex h-full w-full items-center justify-between gap-2 p-3">
        <span className="font-display text-[1.6rem] font-semibold leading-none tracking-tightish text-ink">
          {initials || "·"}
        </span>
        <ShoeGlyph className={SIZES[size]} />
      </div>
    </div>
  );
}

function ShoeGlyph({ className = "" }: { className?: string }) {
  return (
    <svg
      viewBox="0 0 120 80"
      className={`text-ink/80 ${className}`}
      fill="none"
      stroke="currentColor"
      strokeWidth="1.6"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M8 60c10 0 18-6 26-14 6-6 12-10 20-10 6 0 10 4 14 10 4 6 14 10 30 10 8 0 14 4 14 10v6H8v-12z" />
      <path d="M30 60v-8M44 60v-10M58 60v-12M76 60v-8" />
      <path d="M86 50l6-3" />
    </svg>
  );
}

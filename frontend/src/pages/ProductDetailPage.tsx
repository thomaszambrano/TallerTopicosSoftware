import { Link, useNavigate, useParams } from "react-router-dom";
import { ApiError } from "../api/client";
import { getProductById } from "../api/products";
import { ErrorState } from "../components/ErrorState";
import { ProductMark } from "../components/ProductMark";
import { Spinner } from "../components/Spinner";
import { useAsync } from "../hooks/useAsync";
import { formatCurrency } from "../lib/format";

export function ProductDetailPage() {
  const params = useParams<{ id: string }>();
  const navigate = useNavigate();
  const productId = Number(params.id);
  const isValidId = Number.isFinite(productId) && productId > 0;

  const { data, loading, error, reload } = useAsync(
    (signal) => {
      if (!isValidId) {
        return Promise.reject(new ApiError("ID de producto invalido", 400));
      }
      return getProductById(productId, signal);
    },
    [productId],
  );

  if (loading) {
    return (
      <div className="py-12">
        <Spinner label="Cargando producto" />
      </div>
    );
  }

  if (error) {
    const notFound = error instanceof ApiError && error.status === 404;
    return (
      <div className="space-y-6">
        <button type="button" className="btn-ghost -ml-2" onClick={() => navigate(-1)}>
          <ArrowLeft />
          Volver
        </button>
        <ErrorState
          title={notFound ? "Producto no encontrado" : "No pudimos cargar el producto"}
          message={error.message}
          onRetry={notFound ? undefined : reload}
        />
      </div>
    );
  }

  if (!data) return null;

  const inStock = data.stock > 0;

  return (
    <article className="space-y-10">
      <nav
        aria-label="Breadcrumb"
        className="scroll-fade flex items-center gap-2 overflow-x-auto whitespace-nowrap text-xs text-muted"
      >
        <Link to="/" className="underline-link">
          Catalogo
        </Link>
        <span aria-hidden="true">/</span>
        <Link
          to={`/?brand=${encodeURIComponent(data.brand)}`}
          className="underline-link"
        >
          {data.brand}
        </Link>
        <span aria-hidden="true">/</span>
        <span className="text-ink">{data.name}</span>
      </nav>

      <div className="grid gap-10 lg:grid-cols-[minmax(0,1.05fr)_minmax(0,1fr)] lg:items-start">
        <div className="space-y-4">
          <ProductMark
            product={data}
            size="lg"
            className="aspect-[5/4] w-full"
          />
          <dl className="grid grid-cols-2 gap-3 sm:grid-cols-3">
            <DetailItem label="Talla" value={data.size} />
            <DetailItem label="Color" value={data.color} />
            <DetailItem label="Categoria" value={data.category} />
          </dl>
        </div>

        <div className="flex flex-col gap-6 lg:pt-2">
          <header className="space-y-3">
            <p className="eyebrow">{data.brand}</p>
            <h1 className="font-display text-display-xl text-ink">{data.name}</h1>
            <div className="flex items-baseline gap-3">
              <p className="font-display text-2xl font-semibold tracking-tightish text-ink">
                {formatCurrency(data.price)}
              </p>
              <span
                className={[
                  "chip-mono",
                  inStock ? "" : "opacity-80",
                ].join(" ")}
                style={
                  inStock
                    ? undefined
                    : { background: "var(--surface)", color: "var(--muted)" }
                }
              >
                {inStock ? `${data.stock} unidades` : "Agotado"}
              </span>
            </div>
          </header>

          <div className="rule" />

          <p className="max-w-prose text-base leading-relaxed text-ink/90">
            {data.description}
          </p>

          <div className="flex flex-wrap gap-2 pt-2">
            <Link
              to={`/chat?ref=${encodeURIComponent(data.name)}`}
              className="btn-primary"
            >
              Preguntar al asistente
              <ArrowRight />
            </Link>
            <Link to="/" className="btn-outline">
              Seguir explorando
            </Link>
          </div>

          <aside
            className="panel mt-2 grid gap-2 p-4 text-sm sm:grid-cols-[auto_1fr] sm:items-baseline sm:gap-4"
            aria-label="Detalles tecnicos"
          >
            <span className="eyebrow">Stock</span>
            <span className="font-mono text-ink">{data.stock} unidades</span>
            <span className="eyebrow">SKU</span>
            <span className="font-mono text-ink">
              {`${data.brand.slice(0, 3).toUpperCase()}-${String(data.id).padStart(4, "0")}`}
            </span>
          </aside>
        </div>
      </div>
    </article>
  );
}

function DetailItem({ label, value }: { label: string; value: string }) {
  return (
    <div className="panel p-3">
      <p className="eyebrow">{label}</p>
      <p className="mt-1 font-medium text-ink">{value}</p>
    </div>
  );
}

function ArrowLeft() {
  return (
    <svg
      aria-hidden="true"
      viewBox="0 0 16 16"
      className="h-3.5 w-3.5"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.6"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M13 8H3M7 4L3 8l4 4" />
    </svg>
  );
}

function ArrowRight() {
  return (
    <svg
      aria-hidden="true"
      viewBox="0 0 16 16"
      className="h-3.5 w-3.5"
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

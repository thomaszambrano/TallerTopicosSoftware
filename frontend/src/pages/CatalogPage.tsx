import { useCallback, useMemo } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { getProducts } from "../api/products";
import { ErrorState } from "../components/ErrorState";
import { ProductCard } from "../components/ProductCard";
import { Spinner } from "../components/Spinner";
import { useAsync } from "../hooks/useAsync";

export function CatalogPage() {
  const [searchParams, setSearchParams] = useSearchParams();

  const filters = useMemo(
    () => ({
      brand: searchParams.get("brand") ?? undefined,
      category: searchParams.get("category") ?? undefined,
    }),
    [searchParams],
  );

  const {
    data: products,
    loading,
    error,
    reload,
  } = useAsync(
    (signal) => getProducts(filters, signal),
    [filters.brand, filters.category],
  );

  const updateFilter = useCallback(
    (key: "brand" | "category", value: string) => {
      setSearchParams((prev) => {
        const next = new URLSearchParams(prev);
        if (value) {
          next.set(key, value);
        } else {
          next.delete(key);
        }
        return next;
      });
    },
    [setSearchParams],
  );

  const clearFilters = useCallback(() => {
    setSearchParams(new URLSearchParams());
  }, [setSearchParams]);

  const brands = useMemo(() => uniqueValues(products, "brand"), [products]);
  const categories = useMemo(() => uniqueValues(products, "category"), [products]);

  const filtered = products ?? [];
  const featured = filtered[0];
  const rest = filtered.slice(1);
  const hasFilters = Boolean(filters.brand || filters.category);

  return (
    <div className="space-y-12 sm:space-y-14">
      <Hero
        total={filtered.length}
        loading={loading && !products}
      />

      <FilterBar
        brand={filters.brand ?? ""}
        category={filters.category ?? ""}
        brands={brands}
        categories={categories}
        onChange={updateFilter}
        onClear={clearFilters}
        hasFilters={hasFilters}
        disabled={loading && !products}
      />

      {error ? (
        <ErrorState message={error.message} onRetry={reload} />
      ) : loading && !products ? (
        <div className="py-12">
          <Spinner label="Cargando catalogo" />
        </div>
      ) : filtered.length === 0 ? (
        <EmptyState onReset={clearFilters} />
      ) : (
        <div className="space-y-12">
          {featured && !hasFilters ? (
            <section aria-labelledby="featured-heading" className="space-y-4">
              <header className="flex items-baseline justify-between">
                <h2 id="featured-heading" className="eyebrow">
                  Destacado
                </h2>
                <span className="font-mono text-[11px] uppercase tracking-eyebrow text-muted">
                  01 / {filtered.length}
                </span>
              </header>
              <ProductCard product={featured} variant="feature" />
            </section>
          ) : null}

          <section aria-labelledby="grid-heading" className="space-y-5">
            <header className="flex items-baseline justify-between gap-4">
              <h2 id="grid-heading" className="eyebrow">
                {hasFilters ? "Resultados" : "Coleccion"}
              </h2>
              <span className="text-xs text-muted">
                {filtered.length}{" "}
                {filtered.length === 1 ? "producto" : "productos"}
              </span>
            </header>

            <div className="grid grid-cols-1 gap-x-6 gap-y-10 sm:grid-cols-2 lg:grid-cols-3">
              {(hasFilters ? filtered : rest).map((product, index) => (
                <ProductCard
                  key={product.id}
                  product={product}
                  index={hasFilters ? index : index + 1}
                />
              ))}
            </div>
          </section>

          <section className="panel grid gap-4 p-6 sm:grid-cols-[1fr_auto] sm:items-center sm:p-7">
            <div className="space-y-1.5">
              <p className="eyebrow">Necesitas ayuda?</p>
              <p className="font-display text-display-md text-ink">
                Pide una recomendacion al asistente IA.
              </p>
              <p className="max-w-prose text-sm text-muted">
                Cuentale tu uso, marca preferida o talla y te respondera con
                opciones del inventario.
              </p>
            </div>
            <Link to="/chat" className="btn-primary justify-self-start sm:justify-self-end">
              Hablar con el asistente
              <ArrowRight />
            </Link>
          </section>
        </div>
      )}
    </div>
  );
}

interface HeroProps {
  total: number;
  loading: boolean;
}

function Hero({ total, loading }: HeroProps) {
  return (
    <section className="grid gap-6 sm:grid-cols-[minmax(0,1fr)_auto] sm:items-end">
      <div className="space-y-3">
        <p className="eyebrow">Coleccion · primavera</p>
        <h1 className="font-display text-display-xl text-ink">
          Zapatos elegidos
          <br />
          con criterio.
        </h1>
        <p className="max-w-prose text-base leading-relaxed text-muted">
          Una seleccion compacta de modelos para correr, vestir y todos los dias.
          Pregunta a nuestro asistente para encontrar el par exacto.
        </p>
      </div>
      <dl className="flex gap-x-6 sm:flex-col sm:items-end sm:gap-1 sm:text-right">
        <div>
          <dt className="eyebrow">Productos</dt>
          <dd className="font-mono text-base text-ink">
            {loading ? "—" : String(total).padStart(2, "0")}
          </dd>
        </div>
        <div>
          <dt className="eyebrow">Asistente</dt>
          <dd className="font-mono text-base text-ink">Gemini · es-CO</dd>
        </div>
      </dl>
    </section>
  );
}

interface FilterBarProps {
  brand: string;
  category: string;
  brands: string[];
  categories: string[];
  hasFilters: boolean;
  disabled?: boolean;
  onChange: (key: "brand" | "category", value: string) => void;
  onClear: () => void;
}

function FilterBar({
  brand,
  category,
  brands,
  categories,
  hasFilters,
  disabled,
  onChange,
  onClear,
}: FilterBarProps) {
  return (
    <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
      <div className="flex items-baseline gap-3">
        <h2 className="eyebrow">Filtrar</h2>
        {hasFilters ? (
          <span className="font-mono text-[11px] uppercase tracking-eyebrow text-ink">
            activos
          </span>
        ) : null}
      </div>
      <div className="flex flex-wrap items-center gap-2">
        <FilterSelect
          label="Marca"
          value={brand}
          onChange={(v) => onChange("brand", v)}
          options={brands}
          placeholder="Todas las marcas"
          disabled={disabled}
        />
        <FilterSelect
          label="Categoria"
          value={category}
          onChange={(v) => onChange("category", v)}
          options={categories}
          placeholder="Todas las categorias"
          disabled={disabled}
        />
        {hasFilters ? (
          <button type="button" className="btn-ghost" onClick={onClear}>
            Limpiar
          </button>
        ) : null}
      </div>
    </div>
  );
}

interface FilterSelectProps {
  label: string;
  value: string;
  options: string[];
  placeholder: string;
  disabled?: boolean;
  onChange: (value: string) => void;
}

function FilterSelect({
  label,
  value,
  options,
  placeholder,
  disabled,
  onChange,
}: FilterSelectProps) {
  return (
    <label className="relative flex items-center">
      <span className="sr-only">{label}</span>
      <select
        className="input min-w-[10rem] appearance-none pr-9 sm:min-w-[12rem]"
        value={value}
        onChange={(event) => onChange(event.target.value)}
        disabled={disabled}
      >
        <option value="">{placeholder}</option>
        {options.map((option) => (
          <option key={option} value={option}>
            {option}
          </option>
        ))}
      </select>
      <ChevronDown className="pointer-events-none absolute right-3 h-3.5 w-3.5 text-muted" />
    </label>
  );
}

function EmptyState({ onReset }: { onReset: () => void }) {
  return (
    <div className="panel flex flex-col items-start gap-3 p-8">
      <p className="eyebrow">Sin resultados</p>
      <p className="font-display text-display-md text-ink">
        No hay productos que coincidan con esos filtros.
      </p>
      <p className="max-w-prose text-sm text-muted">
        Prueba con menos restricciones o pide al asistente que te sugiera algo.
      </p>
      <div className="flex gap-2 pt-2">
        <button type="button" className="btn-primary" onClick={onReset}>
          Ver todo el catalogo
        </button>
        <Link to="/chat" className="btn-outline">
          Preguntar al asistente
        </Link>
      </div>
    </div>
  );
}

function uniqueValues<T>(items: T[] | undefined, key: keyof T): string[] {
  if (!items) return [];
  const set = new Set<string>();
  for (const item of items) {
    const value = item[key];
    if (typeof value === "string" && value.trim()) {
      set.add(value);
    }
  }
  return Array.from(set).sort((a, b) => a.localeCompare(b));
}

function ChevronDown({ className = "" }: { className?: string }) {
  return (
    <svg
      aria-hidden="true"
      viewBox="0 0 16 16"
      className={className}
      fill="none"
      stroke="currentColor"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M3 6l5 5 5-5" />
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

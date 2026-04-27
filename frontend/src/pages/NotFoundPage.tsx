import { Link } from "react-router-dom";

export function NotFoundPage() {
  return (
    <section className="grid gap-8 py-16 sm:grid-cols-[auto_1fr] sm:items-end sm:py-24">
      <p
        className="font-display text-[clamp(5rem,14vw,11rem)] font-bold leading-none tracking-tightish text-ink"
        aria-hidden="true"
      >
        404
      </p>
      <div className="space-y-3">
        <p className="eyebrow">Pagina no encontrada</p>
        <h1 className="font-display text-display-lg text-ink">
          Lo sentimos, esa ruta no existe.
        </h1>
        <p className="max-w-prose text-sm text-muted">
          Quiza el enlace este desactualizado o lo escribimos diferente. Vuelve al
          catalogo y sigue explorando.
        </p>
        <div className="flex gap-2 pt-2">
          <Link to="/" className="btn-primary">
            Volver al catalogo
          </Link>
          <Link to="/chat" className="btn-outline">
            Hablar con el asistente
          </Link>
        </div>
      </div>
    </section>
  );
}

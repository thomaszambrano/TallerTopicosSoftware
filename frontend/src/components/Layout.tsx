import { NavLink, Outlet } from "react-router-dom";

const navItems = [
  { to: "/", label: "Catalogo", end: true },
  { to: "/chat", label: "Asistente", badge: "IA" },
];

export function Layout() {
  return (
    <div className="flex min-h-full flex-col">
      <SkipLink />
      <SiteHeader />
      <main
        id="main"
        className="mx-auto w-full max-w-page flex-1 px-gutter pb-section pt-8 sm:pt-12"
      >
        <Outlet />
      </main>
      <SiteFooter />
    </div>
  );
}

function SkipLink() {
  return (
    <a
      href="#main"
      className="sr-only focus-visible:not-sr-only focus-visible:fixed focus-visible:left-4 focus-visible:top-4 focus-visible:z-50 focus-visible:rounded focus-visible:bg-ink focus-visible:px-3 focus-visible:py-2 focus-visible:text-[color:var(--accent-ink)]"
    >
      Saltar al contenido
    </a>
  );
}

function SiteHeader() {
  return (
    <header className="sticky top-0 z-30 backdrop-blur-md" style={{ background: "color-mix(in oklch, var(--surface) 88%, transparent)" }}>
      <div className="mx-auto flex max-w-page items-center justify-between px-gutter py-4">
        <NavLink to="/" className="group flex items-baseline gap-3">
          <span className="font-display text-[1.35rem] font-bold leading-none tracking-tightish">
            Shoe Store
          </span>
          <span className="eyebrow hidden sm:inline">est. 2026 · taller topicos</span>
        </NavLink>

        <nav aria-label="Principal" className="flex items-center gap-1.5 sm:gap-3">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.end}
              className={({ isActive }) =>
                [
                  "group relative inline-flex items-center gap-1.5 px-2 py-1.5 text-sm transition-colors",
                  isActive ? "text-ink" : "text-muted hover:text-ink",
                ].join(" ")
              }
            >
              {({ isActive }) => (
                <>
                  <span>{item.label}</span>
                  {item.badge ? (
                    <span className="font-mono text-[10px] uppercase tracking-eyebrow text-muted">
                      {item.badge}
                    </span>
                  ) : null}
                  <span
                    aria-hidden="true"
                    className={[
                      "absolute -bottom-0.5 left-2 right-2 h-px origin-left scale-x-0 transition-transform duration-200 ease-out",
                      isActive ? "scale-x-100" : "group-hover:scale-x-100",
                    ].join(" ")}
                    style={{ background: "var(--ink)" }}
                  />
                </>
              )}
            </NavLink>
          ))}
        </nav>
      </div>
      <div className="rule" />
    </header>
  );
}

function SiteFooter() {
  return (
    <footer className="mt-section">
      <div className="rule" />
      <div className="mx-auto flex max-w-page flex-col gap-4 px-gutter py-8 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p className="font-display text-display-md">Shoe Store</p>
          <p className="mt-1 max-w-prose text-sm text-muted">
            Demo academica · FastAPI + React + Google Gemini AI. Diseno editorial,
            navegacion clara, asistente conversacional.
          </p>
        </div>
        <dl className="grid grid-cols-2 gap-x-8 gap-y-1 text-xs text-muted sm:text-right">
          <dt className="eyebrow">Backend</dt>
          <dd className="font-mono">localhost:8010</dd>
          <dt className="eyebrow">Frontend</dt>
          <dd className="font-mono">vite + react</dd>
        </dl>
      </div>
    </footer>
  );
}

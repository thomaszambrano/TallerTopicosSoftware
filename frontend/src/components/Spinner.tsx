interface SpinnerProps {
  label?: string;
  className?: string;
}

export function Spinner({ label, className = "" }: SpinnerProps) {
  return (
    <div
      className={`flex items-center gap-3 text-muted ${className}`}
      role="status"
      aria-live="polite"
    >
      <span aria-hidden="true" className="relative h-3 w-3">
        <span
          className="absolute inset-0 animate-ping rounded-full opacity-60"
          style={{ background: "var(--ink)" }}
        />
        <span
          className="absolute inset-0.5 rounded-full"
          style={{ background: "var(--ink)" }}
        />
      </span>
      {label ? <span className="font-mono text-xs uppercase tracking-eyebrow">{label}</span> : null}
    </div>
  );
}

interface ErrorStateProps {
  title?: string;
  message: string;
  onRetry?: () => void;
}

export function ErrorState({
  title = "Algo no salio bien",
  message,
  onRetry,
}: ErrorStateProps) {
  return (
    <div role="alert" className="panel flex flex-col gap-3 p-5">
      <div className="flex items-baseline justify-between gap-4">
        <p className="font-display text-display-md text-ink">{title}</p>
        <span className="eyebrow">Error</span>
      </div>
      <p className="max-w-prose text-sm text-muted">{message}</p>
      {onRetry ? (
        <div>
          <button type="button" onClick={onRetry} className="btn-outline">
            Reintentar
          </button>
        </div>
      ) : null}
    </div>
  );
}

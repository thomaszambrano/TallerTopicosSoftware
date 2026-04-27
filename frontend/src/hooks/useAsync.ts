import { useCallback, useEffect, useState } from "react";

export interface AsyncState<T> {
  data: T | undefined;
  loading: boolean;
  error: Error | undefined;
}

export interface UseAsyncResult<T> extends AsyncState<T> {
  reload: () => void;
}

/**
 * Async hook with cancellation support.
 *
 * Notes:
 * - The caller is responsible for declaring `deps` correctly (same contract as useEffect).
 * - On `deps` change the previous data is preserved while the new request is in flight,
 *   which avoids spinner flashes during quick filter changes (stale-while-revalidate).
 * - For an explicit refetch use the returned `reload()` function: it bumps a version
 *   counter and shows a loading indicator on demand.
 */
export function useAsync<T>(
  factory: (signal: AbortSignal) => Promise<T>,
  deps: ReadonlyArray<unknown>,
): UseAsyncResult<T> {
  const [state, setState] = useState<AsyncState<T>>({
    data: undefined,
    loading: true,
    error: undefined,
  });
  const [version, setVersion] = useState(0);

  useEffect(() => {
    const controller = new AbortController();

    factory(controller.signal)
      .then((data) => {
        if (controller.signal.aborted) return;
        setState({ data, loading: false, error: undefined });
      })
      .catch((error: unknown) => {
        if (controller.signal.aborted) return;
        if (error instanceof DOMException && error.name === "AbortError") return;
        setState({
          data: undefined,
          loading: false,
          error: error instanceof Error ? error : new Error(String(error)),
        });
      });

    return () => controller.abort();
    // factory is intentionally excluded; caller controls re-fetch via deps.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [...deps, version]);

  const reload = useCallback(() => {
    setState((prev) => ({ ...prev, loading: true, error: undefined }));
    setVersion((v) => v + 1);
  }, []);

  return { ...state, reload };
}

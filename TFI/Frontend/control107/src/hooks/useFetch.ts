import { useEffect, useState } from "react";

export function useFetch<T>(fn: () => Promise<T>) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fn()
      .then((res) => setData(res))
      .catch(() => setError("Error de conexión con el servidor"))
      .finally(() => setLoading(false));
  }, []);

  return { data, loading, error };
}

import { useEffect, useState } from 'react'

interface Estado<T> {
  data: T | null
  error: string | null
  cargando: boolean
}

// Rutas relativas SIN diagonal inicial (ej. 'api/overview'), requerido por el despliegue
export function useApi<T>(ruta: string | null): Estado<T> {
  const [estado, setEstado] = useState<Estado<T>>({ data: null, error: null, cargando: ruta !== null })

  useEffect(() => {
    if (ruta === null) return
    const ctl = new AbortController()
    setEstado((e) => ({ ...e, cargando: true, error: null }))
    fetch(ruta, { signal: ctl.signal })
      .then((r) => {
        if (!r.ok) throw new Error(`${ruta} -> HTTP ${r.status}`)
        return r.json() as Promise<T>
      })
      .then((data) => setEstado({ data, error: null, cargando: false }))
      .catch((e: Error) => {
        if (e.name !== 'AbortError') setEstado({ data: null, error: e.message, cargando: false })
      })
    return () => ctl.abort()
  }, [ruta])

  return estado
}

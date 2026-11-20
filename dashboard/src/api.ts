import type { AnalisisIA, SolicitudAnalisis } from './types'

// Ruta relativa SIN diagonal inicial (requerido por el despliegue en subruta)
export async function solicitarAnalisis(cuerpo: SolicitudAnalisis): Promise<AnalisisIA> {
  const r = await fetch('api/analisis-ia', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(cuerpo),
  })
  if (!r.ok) throw new Error(`api/analisis-ia -> HTTP ${r.status}`)
  return (await r.json()) as AnalisisIA
}

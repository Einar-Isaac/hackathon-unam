import type { ReactNode } from 'react'

interface Props {
  titulo?: string
  subtitulo?: string
  derecha?: ReactNode
  className?: string
  children: ReactNode
}

// Tarjeta base con efecto cristal esmerilado
export default function GlassCard({ titulo, subtitulo, derecha, className = '', children }: Props) {
  return (
    <section className={`rounded-2xl border border-white/10 bg-white/5 p-5 shadow-2xl backdrop-blur-xl ${className}`}>
      {(titulo || derecha) && (
        <header className="mb-4 flex flex-wrap items-start justify-between gap-3">
          <div>
            <h2 className="text-lg font-semibold text-slate-100">{titulo}</h2>
            {subtitulo && <p className="text-sm text-slate-400">{subtitulo}</p>}
          </div>
          {derecha}
        </header>
      )}
      {children}
    </section>
  )
}

export function Estado({ cargando, error }: { cargando: boolean; error: string | null }) {
  if (error) return <p className="text-sm text-rose-400">Error: {error}</p>
  if (cargando) return <p className="animate-pulse text-sm text-slate-400">Cargando…</p>
  return null
}

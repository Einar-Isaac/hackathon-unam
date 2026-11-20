import type { ReactNode } from 'react'
import type { AnalisisIA } from '../../types'

// Convierte **negritas** del modelo en <b>
function conNegritas(texto: string): ReactNode[] {
  return texto.split('**').map((t, i) => (i % 2 ? <b key={i} className="text-slate-100">{t}</b> : t))
}

// Una viñeta por línea; quita marcadores "-", "•", "*" o "1."
function vinetas(analisis: string): string[] {
  return analisis.split('\n').map((l) => l.trim().replace(/^([-•*]|\d+[.)])\s+/, '')).filter(Boolean)
}

function Insignia({ etiqueta, valor, color }: { etiqueta: string; valor: string; color: string }) {
  return (
    <div className="rounded-lg border border-white/10 bg-white/5 px-2.5 py-1.5">
      <p className="text-[10px] uppercase tracking-wider text-slate-400">{etiqueta}</p>
      <p className="text-sm font-semibold" style={{ color }}>{valor}</p>
    </div>
  )
}

export default function AnalisisResultado({ r }: { r: AnalisisIA }) {
  const i = r.contexto.insignias
  const esJugada = r.contexto.tipo === 'jugada'
  const ttb = i.ttb_s === null ? 'N/D'
    : `${i.ttb_s.toFixed(1)} s${esJugada ? (i.ttb_roto ? ' · rompe' : ' · pase') : ' · mediana'}`

  return (
    <div className="space-y-3">
      <div className="grid grid-cols-2 gap-2">
        <Insignia etiqueta="Disguise Score" valor={i.disguise === null ? 'N/D' : i.disguise.toFixed(1)} color="#f59e0b" />
        <Insignia etiqueta="TTB (tiempo al colapso)" valor={ttb} color="#10b981" />
        <Insignia etiqueta="Cobertura real" valor={i.cobertura} color="#06b6d4" />
        {i.shell && <Insignia etiqueta="Shell al snap" valor={i.shell.split(' ')[0]} color="#cbd5e1" />}
      </div>
      <ul className="space-y-2 text-sm leading-relaxed text-slate-300">
        {vinetas(r.analisis).map((v, k) => (
          <li key={k} className="flex gap-2">
            <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-emerald-400" />
            <span>{conNegritas(v)}</span>
          </li>
        ))}
      </ul>
      {r.aviso && <p className="rounded-lg border border-amber-400/30 bg-amber-400/10 px-3 py-2 text-xs text-amber-200">{r.aviso}</p>}
    </div>
  )
}

import type { Kpis } from '../types'
import GlassCard from './GlassCard'

interface Kpi {
  etiqueta: string
  valor: string
  detalle: string
  contraste?: string
  color: string
}

const pct = (v: number | null, d = 1) => (v === null ? 'N/D' : `${v.toFixed(d)}%`)
const num = (v: number) => v.toLocaleString('es-MX')

function construir(k: Kpis): Kpi[] {
  const { jugadas, supervivencia, engano, ruptura } = k
  const mediana = supervivencia.mediana_colapso_s
  return [
    {
      etiqueta: 'Jugadas analizadas',
      valor: num(jugadas.dropbacks),
      detalle: `dropbacks en ${jugadas.partidos} partidos`,
      contraste: `${num(jugadas.analizadas)} con snap detectado`,
      color: '#06b6d4',
    },
    {
      etiqueta: 'Supervivencia a 2.5 s',
      valor: pct(supervivencia.supervivencia_2_5s * 100),
      detalle: 'bolsillos intactos a los 2.5 s (Kaplan-Meier)',
      contraste: mediana === null ? 'Mediana al colapso: no alcanzada' : `Mediana al colapso: ${mediana.toFixed(1)} s`,
      color: '#10b981',
    },
    {
      etiqueta: 'Impacto del engaño (Disguise ≥ 60)',
      valor: pct(engano.pct_fallido_con_engano),
      detalle: 'de las jugadas disfrazadas terminan en I, INT o sack',
      contraste: `vs ${pct(engano.pct_fallido_sin_engano)} sin engaño`,
      color: '#f59e0b',
    },
    {
      etiqueta: 'Ruptura de bolsillo (< 2 yd)',
      valor: pct(ruptura.pct_ruptura),
      detalle: 'de las jugadas colapsan antes del pase',
      contraste: `Sacks: ${pct(ruptura.pct_sack_con_colapso)} al colapsar vs ${pct(ruptura.pct_sack_sin_colapso)} sin colapso`,
      color: '#fb7185',
    },
  ]
}

export default function KpiCards({ kpis }: { kpis: Kpis }) {
  return (
    <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
      {construir(kpis).map((k) => (
        <GlassCard key={k.etiqueta}>
          <p className="text-xs font-medium uppercase tracking-wider text-slate-400">{k.etiqueta}</p>
          <p className="mt-2 text-4xl font-bold" style={{ color: k.color }}>{k.valor}</p>
          <p className="mt-1 text-sm text-slate-400">{k.detalle}</p>
          {k.contraste && (
            <p className="mt-2 border-t border-white/10 pt-2 text-sm font-medium text-slate-200">{k.contraste}</p>
          )}
        </GlassCard>
      ))}
    </div>
  )
}

import type { Kpis } from '../types'
import GlassCard from './GlassCard'

interface Kpi {
  etiqueta: string
  valor: string
  detalle: string
  color: string
}

export default function KpiCards({ kpis }: { kpis: Kpis }) {
  const items: Kpi[] = [
    {
      etiqueta: 'Disguise Score promedio',
      valor: kpis.disguise_promedio.toFixed(1),
      detalle: `de 100 · ${kpis.n_jugadas.toLocaleString('es-MX')} jugadas analizadas`,
      color: '#f59e0b',
    },
    {
      etiqueta: 'Supervivencia del bolsillo a 2.5 s',
      valor: `${(kpis.supervivencia_2_5s * 100).toFixed(1)}%`,
      detalle: 'probabilidad de que el bolsillo siga limpio (Kaplan-Meier)',
      color: '#10b981',
    },
    {
      etiqueta: 'Cobertura más engañosa',
      valor: kpis.cobertura_mas_enganosa,
      detalle: `Disguise ${kpis.cobertura_disguise_prom.toFixed(1)} · ${kpis.cobertura_n_jugadas} jugadas`,
      color: '#06b6d4',
    },
  ]
  return (
    <div className="grid gap-4 md:grid-cols-3">
      {items.map((k) => (
        <GlassCard key={k.etiqueta}>
          <p className="text-xs font-medium uppercase tracking-wider text-slate-400">{k.etiqueta}</p>
          <p className="mt-2 text-4xl font-bold" style={{ color: k.color }}>{k.valor}</p>
          <p className="mt-1 text-sm text-slate-400">{k.detalle}</p>
        </GlassCard>
      ))}
    </div>
  )
}

import { useEffect, useMemo, useState } from 'react'
import { CartesianGrid, Line, LineChart, ReferenceLine, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import type { AgruparPor, Supervivencia } from '../types'
import { useApi } from '../useApi'
import GlassCard, { Estado } from './GlassCard'

const PALETA = ['#10b981', '#f59e0b', '#06b6d4', '#a78bfa', '#f472b6', '#60a5fa',
  '#facc15', '#34d399', '#fb923c', '#22d3ee', '#c084fc', '#f87171']
const MIN_JUGADAS_VISIBLE = 100 // los grupos con pocas jugadas arrancan ocultos
const OPCIONES: { valor: AgruparPor; texto: string }[] = [
  { valor: 'pff_passCoverage', texto: 'Cobertura Defensiva' },
  { valor: 'offenseFormation', texto: 'Formación Ofensiva' },
]

export default function SurvivalChart() {
  const [agrupar, setAgrupar] = useState<AgruparPor>('pff_passCoverage')
  const { data, error, cargando } = useApi<Supervivencia>(`api/supervivencia?agrupar_por=${agrupar}`)
  const [ocultos, setOcultos] = useState<Set<string>>(new Set())

  useEffect(() => {
    if (data) setOcultos(new Set(data.grupos.filter((g) => g.n_jugadas < MIN_JUGADAS_VISIBLE).map((g) => g.grupo)))
  }, [data])

  // Pivotea las series a una fila por tiempo: { tiempo_s, [grupo]: S(t) }
  const filas = useMemo(() => {
    if (!data || data.grupos.length === 0) return []
    return data.grupos[0].puntos.map((p, i) => {
      const fila: Record<string, number> = { tiempo_s: p.tiempo_s }
      data.grupos.forEach((g) => { fila[g.grupo] = g.puntos[i].supervivencia })
      return fila
    })
  }, [data])

  const alternar = (grupo: string) =>
    setOcultos((prev) => {
      const nuevo = new Set(prev)
      if (nuevo.has(grupo)) nuevo.delete(grupo)
      else nuevo.add(grupo)
      return nuevo
    })

  const selector = (
    <div className="flex rounded-lg border border-white/10 bg-white/5 p-1">
      {OPCIONES.map((o) => (
        <button key={o.valor} onClick={() => setAgrupar(o.valor)}
          className={`rounded-md px-3 py-1 text-sm transition ${agrupar === o.valor
            ? 'bg-emerald-500/20 text-emerald-300' : 'text-slate-400 hover:text-slate-200'}`}>
          {o.texto}
        </button>
      ))}
    </div>
  )

  return (
    <GlassCard titulo="Pocket Survival Curve"
      subtitulo="Probabilidad de que ningún pass rusher llegue a 2.0 yd del QB antes del pase (Kaplan-Meier)"
      derecha={selector}>
      <Estado cargando={cargando} error={error} />
      {data && (
        <>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={filas} margin={{ top: 10, right: 20, left: 0, bottom: 5 }}>
                <CartesianGrid stroke="rgba(255,255,255,0.08)" />
                <XAxis dataKey="tiempo_s" type="number" domain={[0, 4.5]} ticks={[0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5]}
                  stroke="#94a3b8" tickFormatter={(v: number) => `${v}s`} />
                <YAxis domain={[0, 1]} stroke="#94a3b8" tickFormatter={(v: number) => `${Math.round(v * 100)}%`} />
                <Tooltip contentStyle={{ background: 'rgba(15,23,42,0.9)', border: '1px solid rgba(255,255,255,0.15)', borderRadius: 12 }}
                  labelFormatter={(v) => `t = ${v} s`}
                  formatter={(v) => `${(Number(v) * 100).toFixed(1)}%`} />
                <ReferenceLine x={data.umbral_s} stroke="#f59e0b" strokeDasharray="6 4"
                  label={{ value: '2.5 s · umbral de pase', fill: '#f59e0b', position: 'insideBottomLeft', fontSize: 12 }} />
                {data.grupos.map((g, i) => !ocultos.has(g.grupo) && (
                  <Line key={g.grupo} dataKey={g.grupo} stroke={PALETA[i % PALETA.length]}
                    strokeWidth={2} dot={false} type="stepAfter" isAnimationActive={false} />
                ))}
              </LineChart>
            </ResponsiveContainer>
          </div>
          <div className="mt-3 flex flex-wrap gap-2">
            {data.grupos.map((g, i) => (
              <button key={g.grupo} onClick={() => alternar(g.grupo)}
                className={`flex items-center gap-2 rounded-full border border-white/10 px-3 py-1 text-xs transition ${
                  ocultos.has(g.grupo) ? 'opacity-40' : 'bg-white/10'}`}>
                <span className="h-2 w-2 rounded-full" style={{ background: PALETA[i % PALETA.length] }} />
                {g.grupo} <span className="text-slate-400">n={g.n_jugadas}</span>
              </button>
            ))}
          </div>
        </>
      )}
    </GlassCard>
  )
}


import { useMemo, useState } from 'react'
import { Bar, BarChart, CartesianGrid, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import type { RankingRow } from '../types'
import GlassCard from './GlassCard'

type Clave = 'defensiveTeam' | 'disguise_score_prom' | 'pct_exito_engano' | 'n_disfrazadas'
const COLUMNAS: { clave: Clave; texto: string }[] = [
  { clave: 'defensiveTeam', texto: 'Defensa' },
  { clave: 'disguise_score_prom', texto: 'Disguise prom.' },
  { clave: 'pct_exito_engano', texto: '% éxito (I / INT / sack)' },
  { clave: 'n_disfrazadas', texto: 'Jugadas disfrazadas' },
]

export default function DisguiseSection({ ranking }: { ranking: RankingRow[] }) {
  const [orden, setOrden] = useState<{ clave: Clave; desc: boolean }>({ clave: 'disguise_score_prom', desc: true })

  const filas = useMemo(() => {
    const { clave, desc } = orden
    return [...ranking].sort((a, b) => {
      const va = a[clave] ?? -1
      const vb = b[clave] ?? -1
      const c = typeof va === 'string' ? va.localeCompare(vb as string) : (va as number) - (vb as number)
      return desc ? -c : c
    })
  }, [ranking, orden])

  const datos = useMemo(
    () => [...ranking].sort((a, b) => b.disguise_score_prom - a.disguise_score_prom)
      .map((r) => ({ equipo: r.defensiveTeam, disguise: +r.disguise_score_prom.toFixed(1),
        exito: r.pct_exito_engano === null ? 0 : +r.pct_exito_engano.toFixed(1) })),
    [ranking])

  const cambiarOrden = (clave: Clave) =>
    setOrden((o) => ({ clave, desc: o.clave === clave ? !o.desc : clave !== 'defensiveTeam' }))

  return (
    <GlassCard titulo="Disguise Score por Defensa"
      subtitulo="Qué defensas ocultan mejor su cobertura antes del snap y cuántas veces lo convierten en pase incompleto, intercepción o sack">
      <div className="h-72">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={datos} margin={{ top: 5, right: 10, left: 0, bottom: 5 }}>
            <CartesianGrid stroke="rgba(255,255,255,0.08)" vertical={false} />
            <XAxis dataKey="equipo" stroke="#94a3b8" interval={0} fontSize={10} />
            <YAxis stroke="#94a3b8" domain={[0, 100]} />
            <Tooltip cursor={{ fill: 'rgba(255,255,255,0.06)' }}
              contentStyle={{ background: 'rgba(15,23,42,0.9)', border: '1px solid rgba(255,255,255,0.15)', borderRadius: 12 }} />
            <Legend />
            <Bar dataKey="disguise" name="Disguise prom." fill="#f59e0b" radius={[3, 3, 0, 0]} isAnimationActive={false} />
            <Bar dataKey="exito" name="% éxito del engaño" fill="#10b981" radius={[3, 3, 0, 0]} isAnimationActive={false} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="mt-4 max-h-80 overflow-auto rounded-xl border border-white/10">
        <table className="w-full text-left text-sm">
          <thead className="sticky top-0 bg-slate-900/95 text-xs uppercase text-slate-400">
            <tr>
              {COLUMNAS.map((c) => (
                <th key={c.clave} onClick={() => cambiarOrden(c.clave)} className="cursor-pointer px-3 py-2 hover:text-slate-200">
                  {c.texto}{orden.clave === c.clave ? (orden.desc ? ' ▼' : ' ▲') : ''}
                </th>
              ))}
              <th className="px-3 py-2">Cobertura más disfrazada</th>
            </tr>
          </thead>
          <tbody>
            {filas.map((r) => (
              <tr key={r.defensiveTeam} className="border-t border-white/5 hover:bg-white/5">
                <td className="px-3 py-2 font-semibold text-cyan-300">{r.defensiveTeam}</td>
                <td className="px-3 py-2 text-amber-300">{r.disguise_score_prom.toFixed(1)}</td>
                <td className="px-3 py-2 text-emerald-300">{r.pct_exito_engano === null ? '—' : `${r.pct_exito_engano.toFixed(1)}%`}</td>
                <td className="px-3 py-2">{r.n_disfrazadas} / {r.n_jugadas}</td>
                <td className="px-3 py-2">{r.cobertura_mas_disfrazada ?? '—'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </GlassCard>
  )
}


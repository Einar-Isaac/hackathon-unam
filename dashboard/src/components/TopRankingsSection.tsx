import type { ReactNode } from 'react'
import type { PassRusher, RankingRow } from '../types'
import { useApi } from '../useApi'
import GlassCard, { Estado } from './GlassCard'

const TOP = 8
const MIN_SNAPS = 40
const TH = 'px-3 py-2 text-left text-xs font-medium uppercase tracking-wider text-slate-400'
const TD = 'px-3 py-2'

function Tabla({ cabeceras, children }: { cabeceras: string[]; children: ReactNode }) {
  return (
    <div className="overflow-x-auto rounded-xl border border-white/10">
      <table className="w-full text-sm">
        <thead className="bg-white/5">
          <tr>{cabeceras.map((c) => <th key={c} className={TH}>{c}</th>)}</tr>
        </thead>
        <tbody>{children}</tbody>
      </table>
    </div>
  )
}

function DefensasEnganosas({ ranking }: { ranking: RankingRow[] }) {
  const top = [...ranking].sort((a, b) => b.disguise_score_prom - a.disguise_score_prom).slice(0, TOP)
  return (
    <GlassCard titulo="Defensas más engañosas" subtitulo={`Top ${TOP} por Disguise Score promedio`}>
      <Tabla cabeceras={['Equipo', 'Disguise', '% Éxito engaño', 'Cobertura más disfrazada']}>
        {top.map((r) => (
          <tr key={r.defensiveTeam} className="border-t border-white/5 hover:bg-white/5">
            <td className={`${TD} font-semibold text-cyan-300`}>{r.defensiveTeam}</td>
            <td className={`${TD} text-amber-300`}>{r.disguise_score_prom.toFixed(1)}</td>
            <td className={`${TD} text-emerald-300`}>
              {r.pct_exito_engano === null ? '—' : `${r.pct_exito_engano.toFixed(1)}%`}
            </td>
            <td className={TD}>{r.cobertura_mas_disfrazada ?? '—'}</td>
          </tr>
        ))}
      </Tabla>
    </GlassCard>
  )
}

function RushersLetales() {
  const { data, error, cargando } = useApi<PassRusher[]>(`api/pass-rushers?min_snaps=${MIN_SNAPS}&limite=${TOP}`)
  return (
    <GlassCard titulo="Pass rushers más letales"
      subtitulo={`Top ${TOP} por tasa de ruptura < 2 yd (mín. ${MIN_SNAPS} rush snaps)`}>
      <Estado cargando={cargando} error={error} />
      {data && (
        <Tabla cabeceras={['Jugador', '% Ruptura', 'Seg. al colapso', 'H / G / S']}>
          {data.map((r) => (
            <tr key={r.nflId} className="border-t border-white/5 hover:bg-white/5">
              <td className={TD}>
                <span className="font-semibold text-slate-100">{r.displayName ?? r.nflId}</span>
                <span className="ml-2 text-xs text-slate-400">{r.officialPosition ?? ''} · {r.rush_snaps} snaps</span>
              </td>
              <td className={`${TD} text-rose-300`}>{r.pct_ruptura.toFixed(1)}%</td>
              <td className={TD}>{r.seg_prom_colapso === null ? '—' : `${r.seg_prom_colapso.toFixed(2)} s`}</td>
              <td className={`${TD} font-mono text-cyan-300`}>{r.hits} / {r.hurries} / {r.sacks}</td>
            </tr>
          ))}
        </Tabla>
      )}
    </GlassCard>
  )
}

export default function TopRankingsSection({ ranking }: { ranking: RankingRow[] }) {
  return (
    <div className="grid gap-4 lg:grid-cols-2">
      <DefensasEnganosas ranking={ranking} />
      <RushersLetales />
    </div>
  )
}

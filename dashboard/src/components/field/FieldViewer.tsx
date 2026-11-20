import { useEffect, useState } from 'react'
import type { DetalleJugada, JugadaCatalogo } from '../../types'
import { useApi } from '../../useApi'
import GlassCard, { Estado } from '../GlassCard'
import FieldBackground, { ANCHO, LARGO } from './FieldBackground'
import FieldPlayers from './FieldPlayers'
import PlayList from './PlayList'
import { usePlayback } from './usePlayback'

function Insignia({ d }: { d: DetalleJugada }) {
  const engano = d.safeties_snap !== d.safeties_esperados
  return (
    <div className={`rounded-xl border px-4 py-2 text-sm ${engano
      ? 'border-amber-400/40 bg-amber-400/10 text-amber-200'
      : 'border-emerald-400/40 bg-emerald-400/10 text-emerald-200'}`}>
      Al snap parecía: <b>{d.shell_snap ?? 'N/D'}</b> → Real: <b>{d.pff_passCoverage}</b>
      <span className="ml-2 text-xs opacity-80">
        {engano ? 'Disfraz detectado' : 'Shell coherente con la cobertura'} · Disguise {d.disguise_score?.toFixed(1) ?? 'N/D'}
      </span>
    </div>
  )
}

function Visor({ d }: { d: DetalleJugada }) {
  const inicio = 0
  const { indice, setIndice, reproduciendo, alternar } = usePlayback(d.frames.length, inicio)
  const frame = d.frames[Math.min(indice, d.frames.length - 1)]
  const roto = d.frame_ruptura_rel !== null && frame.frame_rel >= d.frame_ruptura_rel

  return (
    <div className="space-y-3">
      <Insignia d={d} />
      <svg viewBox={`0 0 ${LARGO} ${ANCHO}`} className="w-full rounded-xl border border-white/10"
        role="img" aria-label="Cancha táctica 2D">
        <FieldBackground />
        <FieldPlayers frame={frame} frames={d.frames} indice={indice} bolsilloRoto={roto} />
      </svg>

      <div className="flex flex-wrap items-center gap-3">
        <button onClick={alternar}
          className="w-24 rounded-lg bg-emerald-500/20 px-3 py-1.5 text-sm font-medium text-emerald-300 hover:bg-emerald-500/30">
          {reproduciendo ? '⏸ Pause' : '▶ Play'}
        </button>
        <input type="range" min={0} max={d.frames.length - 1} value={indice}
          onChange={(e) => setIndice(Number(e.target.value))} className="min-w-40 flex-1 accent-emerald-500" />
        <span className="w-28 text-right font-mono text-sm text-slate-300">
          t = {frame.tiempo_s >= 0 ? '+' : ''}{frame.tiempo_s.toFixed(1)} s
        </span>
      </div>

      <div className="flex flex-wrap gap-4 text-xs text-slate-400">
        <span className={roto ? 'font-semibold text-rose-400' : 'font-semibold text-emerald-400'}>
          ● Bolsillo {roto ? 'ROTO' : 'limpio'}
          {d.bolsillo_roto && d.tiempo_observado !== null ? ` (ruptura a ${d.tiempo_observado.toFixed(1)} s)` : ''}
        </span>
        <span>{d.possessionTeam} ataca vs {d.defensiveTeam}</span>
        <span>Formación: {d.offenseFormation ?? 'N/D'}</span>
        <span>Resultado: {d.passResult}</span>
        {frame.evento && <span className="text-cyan-300">Evento: {frame.evento}</span>}
      </div>
      <Leyenda />
    </div>
  )
}

function Leyenda() {
  const items: [string, string][] = [['#10b981', 'QB'], ['#06b6d4', 'Ofensiva'], ['#f59e0b', 'Safeties (con trayectoria)'],
    ['#fb7185', 'Pass rushers'], ['#cbd5e1', 'Defensa']]
  return (
    <div className="flex flex-wrap gap-3 text-xs text-slate-400">
      {items.map(([c, t]) => (
        <span key={t} className="flex items-center gap-1">
          <span className="h-2.5 w-2.5 rounded-full" style={{ background: c }} />{t}
        </span>
      ))}
      <span>Círculo punteado = radio de 2.0 yd del QB</span>
    </div>
  )
}

export default function FieldViewer({ onSeleccionar }: { onSeleccionar?: (j: JugadaCatalogo) => void }) {
  const catalogo = useApi<JugadaCatalogo[]>('api/jugadas')
  const [sel, setSel] = useState<{ g: number; p: number } | null>(null)
  const actual = sel ?? (catalogo.data?.length ? { g: catalogo.data[0].gameId, p: catalogo.data[0].playId } : null)
  const jugadaActual = catalogo.data?.find((j) => j.gameId === actual?.g && j.playId === actual?.p) ?? null
  // Informa a la barra lateral IA qué jugada está en pantalla
  useEffect(() => { if (jugadaActual) onSeleccionar?.(jugadaActual) }, [jugadaActual]) // eslint-disable-line react-hooks/exhaustive-deps
  const detalle = useApi<DetalleJugada>(actual ? `api/jugadas/${actual.g}/${actual.p}` : null)

  return (
    <GlassCard titulo="Visor Táctico 2D" subtitulo="Cancha normalizada: la ofensiva ataca de izquierda a derecha">
      <Estado cargando={catalogo.cargando} error={catalogo.error} />
      <div className="grid gap-4 lg:grid-cols-[18rem_1fr]">
        {catalogo.data && actual && (
          <PlayList jugadas={catalogo.data} seleccion={actual}
            onSeleccionar={(g, p) => setSel({ g, p })} />
        )}
        <div>
          <Estado cargando={detalle.cargando} error={detalle.error} />
          {detalle.data && <Visor key={`${detalle.data.gameId}-${detalle.data.playId}`} d={detalle.data} />}
        </div>
      </div>
    </GlassCard>
  )
}


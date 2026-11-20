import { useEffect, useState } from 'react'
import { solicitarAnalisis } from '../api'
import type { AnalisisIA, JugadaCatalogo } from '../types'
import AnalisisResultado from './ai/AnalisisResultado'
import GlassCard from './GlassCard'

type Alcance = 'jugada' | 'cobertura'
const EJEMPLOS = [
  '¿Cómo ataco esta cobertura si el bolsillo dura menos de 2.2 s?',
  '¿Qué debe leer el QB después del snap?',
  '¿Conviene max protect contra este shell?',
]

interface Props {
  jugada: JugadaCatalogo | null
  onCerrar: () => void
}

function Conexion({ r }: { r: AnalisisIA | null }) {
  const [color, texto] = r === null ? ['bg-slate-500', 'Amazon Nova (Bedrock) · sin consultar']
    : r.modo === 'nova' ? ['bg-emerald-400 animate-pulse', `Amazon Nova (Bedrock) · conectado`]
    : ['bg-amber-400', 'Modo offline · respaldo con métricas locales']
  return (
    <p className="flex items-center gap-2 text-xs text-slate-300">
      <span className={`h-2 w-2 rounded-full ${color}`} />{texto}
    </p>
  )
}

export default function TacticalAiSidebar({ jugada, onCerrar }: Props) {
  const [alcance, setAlcance] = useState<Alcance>('jugada')
  const [pregunta, setPregunta] = useState('')
  const [resultado, setResultado] = useState<AnalisisIA | null>(null)
  const [conexion, setConexion] = useState<AnalisisIA | null>(null) // última respuesta, para el indicador
  const [cargando, setCargando] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // Al cambiar la jugada seleccionada, la respuesta anterior deja de aplicar
  useEffect(() => { setResultado(null); setError(null) }, [jugada?.gameId, jugada?.playId, alcance])

  const analizar = async () => {
    if (!jugada) return
    setCargando(true)
    setError(null)
    try {
      const r = await solicitarAnalisis({
        game_id: alcance === 'jugada' ? jugada.gameId : null,
        play_id: alcance === 'jugada' ? jugada.playId : null,
        cobertura: alcance === 'cobertura' ? jugada.pff_passCoverage : null,
        pregunta: pregunta.trim() || null,
      })
      setResultado(r)
      setConexion(r)
    } catch (e) {
      setError((e as Error).message)
    } finally {
      setCargando(false)
    }
  }

  return (
    <GlassCard className="flex h-full flex-col overflow-y-auto"
      titulo="Asistente Táctico IA" subtitulo="Coordinador ofensivo virtual"
      derecha={<button onClick={onCerrar} aria-label="Cerrar" className="text-slate-400 hover:text-slate-100 lg:hidden">✕</button>}>
      <Conexion r={conexion} />

      <div className="mt-4 rounded-xl border border-white/10 bg-white/5 p-3 text-sm">
        <p className="text-xs uppercase tracking-wider text-slate-400">Selección actual</p>
        {jugada ? (
          <>
            <p className="mt-1 font-semibold text-slate-100">{jugada.possessionTeam} vs {jugada.defensiveTeam}</p>
            <p className="text-slate-400">{jugada.pff_passCoverage} · {jugada.offenseFormation ?? 'N/D'} · resultado {jugada.passResult}</p>
          </>
        ) : <p className="mt-1 text-slate-400">Elige una jugada en el visor 2D.</p>}
        <div className="mt-3 flex rounded-lg border border-white/10 p-1">
          {(['jugada', 'cobertura'] as Alcance[]).map((a) => (
            <button key={a} onClick={() => setAlcance(a)}
              className={`flex-1 rounded-md px-2 py-1 text-xs transition ${alcance === a
                ? 'bg-emerald-500/20 text-emerald-300' : 'text-slate-400 hover:text-slate-200'}`}>
              {a === 'jugada' ? 'Esta jugada' : `Toda la ${jugada?.pff_passCoverage ?? 'cobertura'}`}
            </button>
          ))}
        </div>
      </div>

      <label className="mt-4 block text-xs uppercase tracking-wider text-slate-400" htmlFor="pregunta-ia">
        Pregunta del coach (opcional)
      </label>
      <textarea id="pregunta-ia" value={pregunta} onChange={(e) => setPregunta(e.target.value)} maxLength={500} rows={3}
        placeholder="Ej. ¿Cómo atacar esta cobertura si el bolsillo dura menos de 2.2 s?"
        className="mt-1 w-full resize-none rounded-xl border border-white/10 bg-white/5 p-3 text-sm text-slate-100 placeholder:text-slate-500 focus:border-emerald-400/40 focus:outline-none" />
      <div className="mt-2 flex flex-wrap gap-1.5">
        {EJEMPLOS.map((e) => (
          <button key={e} onClick={() => setPregunta(e)}
            className="rounded-full border border-white/10 px-2.5 py-1 text-left text-[11px] text-slate-400 transition hover:border-cyan-400/40 hover:text-cyan-200">
            {e}
          </button>
        ))}
      </div>

      <button onClick={analizar} disabled={!jugada || cargando}
        className="mt-4 w-full rounded-xl bg-emerald-500/20 py-2.5 text-sm font-semibold text-emerald-300 ring-1 ring-emerald-400/30 transition hover:bg-emerald-500/30 disabled:opacity-40">
        {cargando ? 'Analizando…' : 'Analizar Jugada con Nova AI'}
      </button>

      <div className="mt-4">
        {error && <p className="text-sm text-rose-400">Error: {error}</p>}
        {resultado && <AnalisisResultado r={resultado} />}
      </div>
    </GlassCard>
  )
}


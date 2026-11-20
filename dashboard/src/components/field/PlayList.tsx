import type { JugadaCatalogo } from '../../types'

interface Props {
  jugadas: JugadaCatalogo[]
  seleccion: { g: number; p: number }
  onSeleccionar: (gameId: number, playId: number) => void
}

const TITULOS: Record<JugadaCatalogo['tipo_muestra'], string> = {
  alto_disguise: 'Alto disguise',
  ruptura_rapida: 'Ruptura rápida del bolsillo',
}

// Catálogo de las 30 jugadas muestra, agrupadas por tipo
export default function PlayList({ jugadas, seleccion, onSeleccionar }: Props) {
  return (
    <div className="max-h-[34rem] space-y-3 overflow-auto pr-1">
      {(Object.keys(TITULOS) as JugadaCatalogo['tipo_muestra'][]).map((tipo) => (
        <div key={tipo}>
          <p className="mb-1 text-xs font-semibold uppercase tracking-wider text-slate-400">{TITULOS[tipo]}</p>
          <ul className="space-y-1">
            {jugadas.filter((j) => j.tipo_muestra === tipo).map((j) => {
              const activo = j.gameId === seleccion.g && j.playId === seleccion.p
              return (
                <li key={`${j.gameId}-${j.playId}`}>
                  <button onClick={() => onSeleccionar(j.gameId, j.playId)}
                    className={`w-full rounded-lg border px-3 py-2 text-left text-xs transition ${activo
                      ? 'border-emerald-400/50 bg-emerald-400/10' : 'border-white/10 bg-white/5 hover:bg-white/10'}`}>
                    <span className="font-semibold text-slate-100">{j.possessionTeam} vs {j.defensiveTeam}</span>
                    <span className="ml-2 text-amber-300">DS {j.disguise_score?.toFixed(0) ?? '—'}</span>
                    <span className="block text-slate-400">
                      {j.pff_passCoverage} · {j.shell_snap?.split(' ')[0] ?? 'N/D'}
                      {j.bolsillo_roto === 1 && j.tiempo_observado !== null ? ` · rompe ${j.tiempo_observado.toFixed(1)} s` : ''}
                    </span>
                  </button>
                </li>
              )
            })}
          </ul>
        </div>
      ))}
    </div>
  )
}

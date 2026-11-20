import type { Frame, Jugador, Rol } from '../../types'

const RADIO_BOLSILLO = 2.0 // yardas alrededor del QB
const COLOR: Record<Rol, string> = {
  ofensiva: '#06b6d4',
  defensiva: '#cbd5e1',
  pass_rusher: '#fb7185',
  safety: '#f59e0b',
  qb: '#10b981',
  balon: '#a16207',
}

interface Props {
  frame: Frame
  frames: Frame[]          // todos los frames, para trazar la rotación de safeties
  indice: number
  bolsilloRoto: boolean
}

// Trayectoria de cada safety desde el primer frame hasta el actual
function trayectorias(frames: Frame[], indice: number): Record<string, [number, number][]> {
  const out: Record<string, [number, number][]> = {}
  frames.slice(0, indice + 1).forEach((f) =>
    f.jugadores.filter((j) => j.rol === 'safety' && j.id !== null).forEach((j) => {
      (out[String(j.id)] ??= []).push([j.x, j.y])
    }))
  return out
}

function Etiqueta({ j }: { j: Jugador }) {
  return (
    <text x={j.x} y={j.y + 0.35} fontSize={1.1} textAnchor="middle" fill="#0f172a" fontWeight={700}>
      {j.camiseta ?? ''}
    </text>
  )
}

export default function FieldPlayers({ frame, frames, indice, bolsilloRoto }: Props) {
  const qb = frame.jugadores.find((j) => j.rol === 'qb')
  const trazos = trayectorias(frames, indice)
  const colorRadio = bolsilloRoto ? '#ef4444' : '#10b981'

  return (
    <g>
      {/* Radio de 2.0 yd alrededor del QB */}
      {qb && (
        <circle cx={qb.x} cy={qb.y} r={RADIO_BOLSILLO} fill={colorRadio} fillOpacity={0.15}
          stroke={colorRadio} strokeWidth={0.2} strokeDasharray="0.6 0.4" />
      )}
      {/* Rotación de safeties */}
      {Object.entries(trazos).map(([id, pts]) => (
        <g key={id}>
          <polyline points={pts.map((p) => p.join(',')).join(' ')} fill="none"
            stroke="#f59e0b" strokeWidth={0.3} strokeOpacity={0.9} strokeLinecap="round" />
          <circle cx={pts[0][0]} cy={pts[0][1]} r={0.5} fill="none" stroke="#f59e0b" strokeWidth={0.15} />
        </g>
      ))}
      {frame.jugadores.map((j, i) =>
        j.rol === 'balon' ? (
          <ellipse key={`b${i}`} cx={j.x} cy={j.y} rx={0.8} ry={0.5} fill={COLOR.balon} stroke="#fde68a" strokeWidth={0.1} />
        ) : (
          <g key={j.id ?? i}>
            <circle cx={j.x} cy={j.y} r={j.rol === 'safety' || j.rol === 'qb' ? 1.15 : 0.95}
              fill={COLOR[j.rol]} stroke={j.rol === 'safety' ? '#fff' : 'rgba(0,0,0,0.5)'}
              strokeWidth={j.rol === 'safety' ? 0.25 : 0.12} />
            <Etiqueta j={j} />
          </g>
        ))}
    </g>
  )
}

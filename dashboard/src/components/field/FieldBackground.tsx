// Cancha 120 x 53.3 yd (unidades SVG = yardas). Ataque de izquierda a derecha.
export const LARGO = 120
export const ANCHO = 53.3

const lineas = Array.from({ length: 23 }, (_, i) => 5 + i * 5) // 5..115 cada 5 yd

export default function FieldBackground() {
  return (
    <g>
      <rect x={0} y={0} width={LARGO} height={ANCHO} fill="#064e3b" />
      {/* Zonas de anotación */}
      <rect x={0} y={0} width={10} height={ANCHO} fill="#0e7490" fillOpacity={0.45} />
      <rect x={110} y={0} width={10} height={ANCHO} fill="#b45309" fillOpacity={0.4} />
      {/* Líneas cada 5 yd (más gruesas cada 10) */}
      {lineas.map((x) => (
        <line key={x} x1={x} x2={x} y1={0} y2={ANCHO}
          stroke="white" strokeOpacity={x % 10 === 0 ? 0.5 : 0.18} strokeWidth={x % 10 === 0 ? 0.18 : 0.1} />
      ))}
      {/* Números de yarda cada 10 yd dentro del campo: 10,20,...,50,...,10 */}
      {[20, 30, 40, 50, 60, 70, 80, 90, 100].map((x) => {
        const n = x <= 60 ? x - 10 : 110 - x
        return (
          <g key={x} fill="white" fillOpacity={0.35} fontSize={3} textAnchor="middle" fontWeight={700}>
            <text x={x} y={9}>{n}</text>
            <text x={x} y={ANCHO - 6} >{n}</text>
          </g>
        )
      })}
      {/* Hash marks */}
      {Array.from({ length: 101 }, (_, i) => 10 + i).map((x) => (
        <g key={x} stroke="white" strokeOpacity={0.3} strokeWidth={0.1}>
          <line x1={x} x2={x} y1={ANCHO / 2 - 3.1} y2={ANCHO / 2 - 2.5} />
          <line x1={x} x2={x} y1={ANCHO / 2 + 2.5} y2={ANCHO / 2 + 3.1} />
        </g>
      ))}
      <text x={5} y={ANCHO / 2} fill="white" fillOpacity={0.3} fontSize={3} textAnchor="middle"
        transform={`rotate(-90 5 ${ANCHO / 2})`}>ZONA DE ANOTACIÓN</text>
      <text x={115} y={ANCHO / 2} fill="white" fillOpacity={0.3} fontSize={3} textAnchor="middle"
        transform={`rotate(90 115 ${ANCHO / 2})`}>ZONA DE ANOTACIÓN</text>
      <rect x={0} y={0} width={LARGO} height={ANCHO} fill="none" stroke="white" strokeOpacity={0.6} strokeWidth={0.2} />
    </g>
  )
}

import { useEffect, useState } from 'react'

const MS_POR_FRAME = 100 // los datos están a 10 Hz: reproducción en tiempo real

// Controla el índice de frame y la reproducción automática
export function usePlayback(total: number, inicio: number) {
  const [indice, setIndice] = useState(inicio)
  const [reproduciendo, setReproduciendo] = useState(false)

  // Al cambiar de jugada se reinicia en el frame inicial
  useEffect(() => {
    setIndice(inicio)
    setReproduciendo(false)
  }, [total, inicio])

  useEffect(() => {
    if (!reproduciendo) return
    const id = setInterval(() => {
      setIndice((i) => {
        if (i >= total - 1) {
          setReproduciendo(false)
          return i
        }
        return i + 1
      })
    }, MS_POR_FRAME)
    return () => clearInterval(id)
  }, [reproduciendo, total])

  const alternar = () => {
    if (!reproduciendo && indice >= total - 1) setIndice(inicio) // reinicia si terminó
    setReproduciendo((r) => !r)
  }
  return { indice, setIndice, reproduciendo, alternar }
}

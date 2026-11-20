import { useState } from 'react'
import DisguiseSection from './components/DisguiseSection'
import FieldViewer from './components/field/FieldViewer'
import { Estado } from './components/GlassCard'
import KpiCards from './components/KpiCards'
import SurvivalChart from './components/SurvivalChart'
import TacticalAiSidebar from './components/TacticalAiSidebar'
import TopRankingsSection from './components/TopRankingsSection'
import type { JugadaCatalogo, Overview } from './types'
import { useApi } from './useApi'

export default function App() {
  const { data, error, cargando } = useApi<Overview>('api/overview')
  const [jugada, setJugada] = useState<JugadaCatalogo | null>(null)
  const [panelAbierto, setPanelAbierto] = useState(false) // drawer en pantallas pequeñas

  return (
    <div className="relative min-h-screen overflow-hidden bg-slate-950 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-emerald-950/40 via-slate-950 to-slate-950 text-slate-100">
      {/* Luces ambientales sutiles */}
      <div className="pointer-events-none absolute -left-40 -top-40 h-[32rem] w-[32rem] rounded-full bg-emerald-500/10 blur-3xl" />
      <div className="pointer-events-none absolute -right-40 top-1/3 h-[30rem] w-[30rem] rounded-full bg-cyan-500/10 blur-3xl" />
      <div className="pointer-events-none absolute bottom-0 left-1/3 h-[26rem] w-[26rem] rounded-full bg-amber-500/5 blur-3xl" />

      <div className="relative mx-auto grid max-w-[1600px] gap-6 p-4 md:p-8 lg:grid-cols-12">
        <main className="min-w-0 space-y-6 lg:col-span-8">
          <header>
            <p className="text-xs font-semibold uppercase tracking-[0.3em] text-emerald-400">NFL Big Data Bowl 2026 · UNAM</p>
            <h1 className="mt-1 text-3xl font-bold md:text-4xl">Pocket Intelligence</h1>
            <p className="mt-1 max-w-3xl text-slate-400">
              Panel táctico para Coordinadores Ofensivos y Quarterbacks: qué tan bien disfrazan las defensas su cobertura
              antes del snap y cuánto tiempo sobrevive el bolsillo.
            </p>
          </header>

          <Estado cargando={cargando} error={error} />
          {data && (
            <>
              <KpiCards kpis={data.kpis} />
              <SurvivalChart />
              <DisguiseSection ranking={data.ranking} />
              <TopRankingsSection ranking={data.ranking} />
            </>
          )}
          <FieldViewer onSeleccionar={setJugada} />
        </main>

        {/* Barra lateral: fija en desktop, drawer deslizable en móvil */}
        <aside className={`fixed inset-y-0 right-0 z-40 w-[92%] max-w-md p-3 transition-transform duration-300
          lg:static lg:z-auto lg:col-span-4 lg:w-auto lg:max-w-none lg:translate-x-0 lg:p-0
          ${panelAbierto ? 'translate-x-0' : 'translate-x-full'}`}>
          <div className="h-full lg:sticky lg:top-6 lg:h-[calc(100vh-3rem)]">
            <TacticalAiSidebar jugada={jugada} onCerrar={() => setPanelAbierto(false)} />
          </div>
        </aside>
        <button onClick={() => setPanelAbierto(true)}
          className="fixed bottom-4 right-4 z-30 rounded-full border border-emerald-400/30 bg-slate-900/80 px-4 py-2 text-sm font-medium text-emerald-300 shadow-lg backdrop-blur-xl lg:hidden">
          ✦ Asistente IA
        </button>
      </div>
    </div>
  )
}

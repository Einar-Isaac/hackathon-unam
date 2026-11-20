import DisguiseSection from './components/DisguiseSection'
import FieldViewer from './components/field/FieldViewer'
import { Estado } from './components/GlassCard'
import KpiCards from './components/KpiCards'
import SurvivalChart from './components/SurvivalChart'
import TopRankingsSection from './components/TopRankingsSection'
import type { Overview } from './types'
import { useApi } from './useApi'

export default function App() {
  const { data, error, cargando } = useApi<Overview>('api/overview')

  return (
    <div className="relative min-h-screen overflow-hidden bg-slate-950 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-emerald-950/40 via-slate-950 to-slate-950 text-slate-100">
      {/* Degradados sutiles de fondo */}
      <div className="pointer-events-none absolute -left-40 -top-40 h-[32rem] w-[32rem] rounded-full bg-emerald-500/10 blur-3xl" />
      <div className="pointer-events-none absolute -right-40 top-1/3 h-[30rem] w-[30rem] rounded-full bg-cyan-500/10 blur-3xl" />
      <div className="pointer-events-none absolute bottom-0 left-1/3 h-[26rem] w-[26rem] rounded-full bg-amber-500/5 blur-3xl" />

      <main className="relative mx-auto max-w-7xl space-y-6 p-4 md:p-8">
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
        <FieldViewer />
      </main>
    </div>
  )
}


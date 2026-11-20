"""Script de solo lectura: imprime los 5 hallazgos del pitch desde data/pocket.db.

Ejecuta desde la raíz: .venv\\Scripts\\python.exe -m backend.hallazgos
"""
import sys

import pandas as pd

from backend import repositorio
from backend.pipeline.config import RESULTADOS_EXITO, UMBRAL_DISGUISE
from backend.servicios.utiles import etiqueta_shell

MIN_JUGADAS_COBERTURA = 100  # evita comparar coberturas con muestra minúscula
MIN_RUSH_SNAPS = 40


def _pct_fallido(jm: pd.DataFrame) -> float:
    return float(100 * jm["passResult"].isin(RESULTADOS_EXITO).mean())


def hallazgo_1(jm: pd.DataFrame) -> None:
    print("\n[1] TOP 3 DEFENSAS CON MAYOR DISGUISE SCORE")
    evaluables = jm.dropna(subset=["disguise_score"])
    for _, r in repositorio.ranking().head(3).iterrows():
        eq = evaluables[evaluables["defensiveTeam"] == r["defensiveTeam"]]
        sin = eq[eq["disguise_score"] < UMBRAL_DISGUISE]
        print(f"  {r['defensiveTeam']}: Disguise {r['disguise_score_prom']:.1f} | "
              f"fallan {r['pct_exito_engano']:.1f}% con engaño ({int(r['n_disfrazadas'])} jugadas) "
              f"vs {_pct_fallido(sin):.1f}% sin engaño ({len(sin)} jugadas)")


def hallazgo_2(jm: pd.DataFrame) -> None:
    print("\n[2] COBERTURA MÁS ENGAÑOSA (mín. 30 jugadas)")
    ev = jm.dropna(subset=["disguise_score"])
    por_cob = ev.groupby("pff_passCoverage")["disguise_score"].agg(["mean", "size"])
    por_cob = por_cob[por_cob["size"] >= 30].sort_values("mean", ascending=False)
    cob = por_cob.index[0]
    sub = ev[ev["pff_passCoverage"] == cob]
    print(f"  {cob}: Disguise {por_cob.loc[cob, 'mean']:.1f} en {len(sub)} jugadas "
          f"(2.º lugar: {por_cob.index[1]} {por_cob.iloc[1]['mean']:.1f})")
    esperado = etiqueta_shell(sub["safeties_esperados"].iloc[0])
    print(f"  Shell esperado para {cob}: {esperado}")
    print("  Shell mostrado al snap:")
    for n, pct in (100 * sub["safeties_snap"].value_counts(normalize=True)).sort_index().items():
        print(f"    {etiqueta_shell(n)}: {pct:.1f}%")
    print(f"  Jugadas con engaño (Disguise ≥ 60): {100 * (sub['disguise_score'] >= UMBRAL_DISGUISE).mean():.1f}%")


def hallazgo_3() -> None:
    print("\n[3] SUPERVIVENCIA DEL BOLSILLO A 2.5 s")
    for variable, titulo in (("pff_passCoverage", "Por cobertura"), ("offenseFormation", "Por formación")):
        c = repositorio.curvas(variable)
        s = c[c["tiempo_s"] == 2.5][["grupo", "supervivencia", "n_jugadas"]]
        s = s[s["n_jugadas"] >= MIN_JUGADAS_COBERTURA].sort_values("supervivencia")
        print(f"  {titulo} (grupos con ≥ {MIN_JUGADAS_COBERTURA} jugadas):")
        for r in s.itertuples():
            print(f"    {r.grupo:<12} {100 * r.supervivencia:5.1f}%  (n={r.n_jugadas})")
        peor, mejor = s.iloc[0], s.iloc[-1]
        print(f"  -> Mejor: {mejor['grupo']} {100 * mejor['supervivencia']:.1f}% | "
              f"Peor: {peor['grupo']} {100 * peor['supervivencia']:.1f}% | "
              f"brecha {100 * (mejor['supervivencia'] - peor['supervivencia']):.1f} pts")


def hallazgo_4() -> None:
    print(f"\n[4] TOP 3 PASS RUSHERS (tasa de ruptura < 2 yd, mín. {MIN_RUSH_SNAPS} rush snaps)")
    for r in repositorio.ranking_rushers(MIN_RUSH_SNAPS, 3).itertuples():
        print(f"  {r.displayName} ({r.officialPosition}): {r.pct_ruptura:.1f}% de ruptura, "
              f"{r.seg_prom_colapso:.2f} s promedio al colapso | {r.rush_snaps} snaps | "
              f"H/G/S {int(r.hits)}/{int(r.hurries)}/{int(r.sacks)}")


def main() -> None:
    jm = repositorio.jugadas_metricas()
    print(f"Base: {len(jm)} jugadas analizadas (lectura solo, sin modificar pocket.db)")
    hallazgo_1(jm)
    hallazgo_2(jm)
    hallazgo_3()
    hallazgo_4()


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()

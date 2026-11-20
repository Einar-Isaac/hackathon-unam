"""Ranking de defensas por capacidad de disfrazar coberturas."""
import pandas as pd

from backend.pipeline.config import RESULTADOS_EXITO, UMBRAL_DISGUISE


def ranking_defensas(jm: pd.DataFrame) -> pd.DataFrame:
    """Agrupa por defensiveTeam: disguise promedio, % de éxito y cobertura más disfrazada.

    % éxito = de las jugadas con disguise_score >= 60, las que terminan en I, IN o S.
    """
    evaluables = jm.dropna(subset=["disguise_score"]).copy()
    evaluables["disfrazada"] = evaluables["disguise_score"] >= UMBRAL_DISGUISE
    evaluables["exito"] = evaluables["disfrazada"] & evaluables["passResult"].isin(RESULTADOS_EXITO)

    filas = []
    for equipo, g in evaluables.groupby("defensiveTeam"):
        disf = g[g["disfrazada"]]
        moda = disf["pff_passCoverage"].mode()
        filas.append({
            "defensiveTeam": equipo,
            "n_jugadas": len(g),
            "disguise_score_prom": g["disguise_score"].mean(),
            "n_disfrazadas": len(disf),
            "pct_exito_engano": 100 * disf["exito"].sum() / len(disf) if len(disf) else None,
            # moda().sort_values garantiza desempates deterministas
            "cobertura_mas_disfrazada": moda.sort_values().iloc[0] if not moda.empty else None,
        })
    ranking = pd.DataFrame(filas)
    return ranking.sort_values("disguise_score_prom", ascending=False).reset_index(drop=True)

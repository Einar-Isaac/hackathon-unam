"""KPIs globales del tablero."""
from functools import lru_cache

from backend import repositorio
from backend.pipeline.kaplan_meier import kaplan_meier
from backend.servicios.utiles import a_registros

UMBRAL_PASE_S = 2.5
MIN_JUGADAS_COBERTURA = 30  # evita coronar coberturas con muestra minúscula


@lru_cache(maxsize=1)
def calcular_overview() -> dict:
    """Disguise promedio, supervivencia global a 2.5 s, cobertura más engañosa y ranking."""
    jm = repositorio.jugadas_metricas()

    surv = jm.dropna(subset=["tiempo_observado", "bolsillo_roto"])
    curva = kaplan_meier(surv["tiempo_observado"].to_numpy(), surv["bolsillo_roto"].to_numpy())
    s25 = float(curva.loc[curva["tiempo_s"] == UMBRAL_PASE_S, "supervivencia"].iloc[0])

    cob = (jm.dropna(subset=["disguise_score"]).groupby("pff_passCoverage")["disguise_score"]
           .agg(["mean", "size"]))
    cob = cob[cob["size"] >= MIN_JUGADAS_COBERTURA].sort_values("mean", ascending=False)
    top = cob.iloc[0]

    return {
        "kpis": {
            "disguise_promedio": float(jm["disguise_score"].mean()),
            "supervivencia_2_5s": s25,
            "cobertura_mas_enganosa": cob.index[0],
            "cobertura_disguise_prom": float(top["mean"]),
            "cobertura_n_jugadas": int(top["size"]),
            "n_jugadas": int(len(jm)),
        },
        "ranking": a_registros(repositorio.ranking()),
    }

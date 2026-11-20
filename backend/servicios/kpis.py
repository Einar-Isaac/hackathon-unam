"""KPIs globales del tablero."""
from functools import lru_cache

import pandas as pd

from backend import repositorio
from backend.pipeline.config import RESULTADOS_EXITO, UMBRAL_DISGUISE
from backend.pipeline.kaplan_meier import kaplan_meier, mediana_km
from backend.servicios.utiles import a_registros

UMBRAL_PASE_S = 2.5


def _pct(serie_bool: pd.Series) -> float | None:
    """Porcentaje de True; None si no hay datos."""
    return float(100 * serie_bool.mean()) if len(serie_bool) else None


def _kpi_jugadas() -> dict:
    meta = repositorio.metadatos().iloc[0]
    return {"dropbacks": int(meta["n_dropbacks"]), "partidos": int(meta["n_partidos"]),
            "analizadas": int(meta["n_analizadas"])}


def _kpi_supervivencia(jm: pd.DataFrame) -> dict:
    d = jm.dropna(subset=["tiempo_observado", "bolsillo_roto"])
    t, ev = d["tiempo_observado"].to_numpy(), d["bolsillo_roto"].to_numpy()
    curva = kaplan_meier(t, ev)
    s25 = curva.loc[curva["tiempo_s"] == UMBRAL_PASE_S, "supervivencia"].iloc[0]
    return {"supervivencia_2_5s": float(s25), "mediana_colapso_s": mediana_km(t, ev)}


def _kpi_engano(jm: pd.DataFrame) -> dict:
    d = jm.dropna(subset=["disguise_score"])
    fallido = d["passResult"].isin(RESULTADOS_EXITO)
    con = d["disguise_score"] >= UMBRAL_DISGUISE
    return {"pct_fallido_con_engano": _pct(fallido[con]), "pct_fallido_sin_engano": _pct(fallido[~con]),
            "n_con_engano": int(con.sum()), "n_sin_engano": int((~con).sum())}


def _kpi_ruptura(jm: pd.DataFrame) -> dict:
    d = jm.dropna(subset=["bolsillo_roto"])
    roto = d["bolsillo_roto"] == 1
    sack = d["passResult"] == "S"
    return {"pct_ruptura": _pct(roto), "pct_sack_con_colapso": _pct(sack[roto]),
            "pct_sack_sin_colapso": _pct(sack[~roto]), "n_con_colapso": int(roto.sum())}


@lru_cache(maxsize=1)
def calcular_overview() -> dict:
    """KPIs de las 4 tarjetas y ranking completo de defensas por disguise."""
    jm = repositorio.jugadas_metricas()
    return {
        "kpis": {"jugadas": _kpi_jugadas(), "supervivencia": _kpi_supervivencia(jm),
                 "engano": _kpi_engano(jm), "ruptura": _kpi_ruptura(jm)},
        "ranking": a_registros(repositorio.ranking()),
    }

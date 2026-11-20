"""Métrica 1: disguise_score (0-100) a partir de la formación de safeties al snap."""
import numpy as np
import pandas as pd

from backend.pipeline.config import (
    FACTOR_MOVIMIENTO, FRAMES_1S, POSICIONES_SAFETY, PROFUNDIDAD_MIN,
    PUNTOS_DESAJUSTE, PUNTOS_MAX_MOVIMIENTO, SAFETIES_ESPERADOS,
    Y_MAX_PROFUNDO, Y_MIN_PROFUNDO,
)

SIN_DATOS = {"safeties_snap": np.nan, "safeties_esperados": np.nan,
             "desplazamiento_safeties_1s": np.nan, "disguise_score": np.nan}


def _safeties_al_snap(snap: pd.DataFrame) -> pd.DataFrame:
    """Defensivos FS/SS por posición oficial o por alineación PFF."""
    pos_pff = snap["pff_positionLinedUp"].fillna("").str.startswith(POSICIONES_SAFETY)
    es_safety = snap["officialPosition"].isin(POSICIONES_SAFETY) | pos_pff
    return snap[es_safety & snap["team"].eq(snap["defensiveTeam"])]


def _desplazamiento_1s(jugada: pd.DataFrame, safeties: pd.DataFrame, f_snap: int) -> float:
    """Desplazamiento promedio (yardas) de los safeties 10 frames tras el snap."""
    if safeties.empty:
        return 0.0
    f_obj = min(f_snap + FRAMES_1S, int(jugada["frameId"].max()))
    despues = jugada[(jugada["frameId"] == f_obj) & jugada["nflId"].isin(safeties["nflId"])]
    par = safeties[["nflId", "x", "y"]].merge(despues[["nflId", "x", "y"]], on="nflId",
                                              suffixes=("_0", "_1"), validate="1:1")
    if par.empty:
        return np.nan
    return float(np.hypot(par["x_1"] - par["x_0"], par["y_1"] - par["y_0"]).mean())


def calcular_disguise(jugada: pd.DataFrame, f_snap: int, cobertura: str | float) -> dict:
    """Devuelve safeties al snap/esperados, desplazamiento y disguise_score.

    Coberturas fuera del mapa esperado (Red Zone, Prevent, etc.) no son evaluables: NaN.
    """
    snap = jugada[jugada["frameId"] == f_snap]
    balon = snap.loc[snap["team"] == "football", "x"]
    esperados = SAFETIES_ESPERADOS.get(cobertura)
    if balon.empty or esperados is None:
        return dict(SIN_DATOS)

    safeties = _safeties_al_snap(snap)
    profundos = ((safeties["x"] - balon.iloc[0] > PROFUNDIDAD_MIN)
                 & safeties["y"].between(Y_MIN_PROFUNDO, Y_MAX_PROFUNDO))
    n_snap = int(profundos.sum())
    desplaz = _desplazamiento_1s(jugada, safeties, f_snap)

    puntos = PUNTOS_DESAJUSTE if n_snap != esperados else 0.0
    puntos += min(PUNTOS_MAX_MOVIMIENTO, desplaz * FACTOR_MOVIMIENTO)
    return {"safeties_snap": n_snap, "safeties_esperados": esperados,
            "desplazamiento_safeties_1s": desplaz, "disguise_score": puntos}

"""Estimador Kaplan-Meier S(t) = prod(1 - d_i / n_i) con numpy/pandas."""
import numpy as np
import pandas as pd

from backend.pipeline.config import SEG_POR_FRAME, T_MAX_KM

PASOS = int(round(T_MAX_KM / SEG_POR_FRAME))  # 45 -> grilla 0.0 ... 4.5 s


def kaplan_meier(tiempos: np.ndarray, eventos: np.ndarray) -> pd.DataFrame:
    """Evalúa S(t) en la grilla de 0.1 s. `eventos`: 1 = ruptura, 0 = censurado."""
    # Tiempos como enteros (décimas de segundo) para evitar errores de coma flotante
    idx = np.rint(np.asarray(tiempos) / SEG_POR_FRAME).astype(int)
    ev = np.asarray(eventos).astype(int)
    largo = max(PASOS, int(idx.max())) + 1

    d = np.bincount(idx[ev == 1], minlength=largo)               # rupturas en t_i
    en_riesgo = np.bincount(idx, minlength=largo)[::-1].cumsum()[::-1]  # n_i: T >= t_i
    factor = np.ones(largo)
    hay = en_riesgo > 0
    factor[hay] = 1.0 - d[hay] / en_riesgo[hay]
    surv = np.cumprod(factor)[: PASOS + 1]
    return pd.DataFrame({
        "tiempo_s": np.round(np.arange(PASOS + 1) * SEG_POR_FRAME, 1),
        "supervivencia": surv,
        "n_en_riesgo": en_riesgo[: PASOS + 1],
    })


def curvas_por_grupo(jm: pd.DataFrame, variable: str) -> pd.DataFrame:
    """Una curva KM por cada valor de `variable` (pff_passCoverage, offenseFormation)."""
    datos = jm.dropna(subset=[variable, "tiempo_observado", "bolsillo_roto"])
    partes = []
    for grupo, g in datos.groupby(variable):
        curva = kaplan_meier(g["tiempo_observado"].to_numpy(), g["bolsillo_roto"].to_numpy())
        curva.insert(0, "grupo", grupo)
        curva.insert(0, "variable", variable)
        curva["n_jugadas"] = len(g)
        partes.append(curva)
    return pd.concat(partes, ignore_index=True)

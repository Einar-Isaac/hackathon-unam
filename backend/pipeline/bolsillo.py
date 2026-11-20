"""Métrica 2: tiempo hasta ruptura del bolsillo (dato de supervivencia censurado)."""
import numpy as np
import pandas as pd

from backend.pipeline.config import (
    DISTANCIA_ROMPE, EVENTOS_PASE, EVENTOS_SACK, SEG_POR_FRAME,
)


def _distancia_minima_por_frame(ventana: pd.DataFrame) -> pd.Series:
    """Distancia mínima entre cualquier pass rusher y el QB, indexada por frame."""
    rol = ventana["pff_role"].str.lower()
    qb = ventana.loc[rol == "pass", ["frameId", "x", "y"]]
    rush = ventana.loc[rol == "pass rush", ["frameId", "x", "y"]]
    if qb.empty or rush.empty:
        return pd.Series(dtype=float)
    # validate asegura un solo QB por frame (no se duplican filas de rushers)
    j = rush.merge(qb, on="frameId", suffixes=("", "_qb"), validate="m:1")
    j["dist"] = np.hypot(j["x"] - j["x_qb"], j["y"] - j["y_qb"])
    return j.groupby("frameId")["dist"].min().sort_index()


def calcular_bolsillo(jugada: pd.DataFrame, f_snap: int, f_fin: int, evento_fin: str) -> dict:
    """Calcula tiempo_observado (s) y bolsillo_roto (1 evento, 0 censurado).

    Un sack sin cruce previo de 2.0 yardas se cuenta como ruptura en el frame del sack.
    """
    # En pases el frame del lanzamiento no cuenta: la ruptura debe ser "antes de lanzar"
    ultimo = f_fin - 1 if evento_fin in EVENTOS_PASE else f_fin
    ventana = jugada[(jugada["frameId"] >= f_snap) & (jugada["frameId"] <= ultimo)]
    dist = _distancia_minima_por_frame(ventana)
    if dist.empty:
        return {"tiempo_observado": np.nan, "bolsillo_roto": np.nan}

    cruces = dist[dist < DISTANCIA_ROMPE]
    if not cruces.empty:
        frame_evento, roto = int(cruces.index[0]), 1
    elif evento_fin in EVENTOS_SACK:
        frame_evento, roto = f_fin, 1
    else:
        frame_evento, roto = f_fin, 0  # censura a la derecha
    return {"tiempo_observado": round((frame_evento - f_snap) * SEG_POR_FRAME, 1),
            "bolsillo_roto": roto}

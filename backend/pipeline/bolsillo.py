"""Métrica 2: tiempo hasta ruptura del bolsillo (dato de supervivencia censurado)."""
import numpy as np
import pandas as pd

from backend.pipeline.config import DISTANCIA_ROMPE, EVENTOS_SACK, SEG_POR_FRAME
from backend.pipeline.distancias import distancias_rusher_qb
from backend.pipeline.eventos import ventana_observada


def calcular_bolsillo(jugada: pd.DataFrame, f_snap: int, f_fin: int, evento_fin: str) -> dict:
    """Calcula tiempo_observado (s) y bolsillo_roto (1 evento, 0 censurado).

    Un sack sin cruce previo de 2.0 yardas se cuenta como ruptura en el frame del sack.
    """
    dist = distancias_rusher_qb(ventana_observada(jugada, f_snap, f_fin, evento_fin))
    if dist.empty:
        return {"tiempo_observado": np.nan, "bolsillo_roto": np.nan}

    minima = dist.groupby("frameId")["dist"].min().sort_index()
    cruces = minima[minima < DISTANCIA_ROMPE]
    if not cruces.empty:
        frame_evento, roto = int(cruces.index[0]), 1
    elif evento_fin in EVENTOS_SACK:
        frame_evento, roto = f_fin, 1
    else:
        frame_evento, roto = f_fin, 0  # censura a la derecha
    return {"tiempo_observado": round((frame_evento - f_snap) * SEG_POR_FRAME, 1),
            "bolsillo_roto": roto}

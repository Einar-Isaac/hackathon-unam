"""Normalización espacial: la ofensiva siempre ataca de izquierda a derecha."""
import numpy as np
import pandas as pd

from backend.pipeline.config import ANCHO_CAMPO, LARGO_CAMPO


def normalizar_direccion(trk: pd.DataFrame) -> pd.DataFrame:
    """Refleja x, y, dir y o cuando playDirection == 'left'. Devuelve una copia."""
    out = trk.copy()
    izq = out["playDirection"].eq("left")
    out["x"] = np.where(izq, LARGO_CAMPO - out["x"], out["x"])
    out["y"] = np.where(izq, ANCHO_CAMPO - out["y"], out["y"])
    for col in ("dir", "o"):  # NaN se conserva (balón no tiene orientación)
        out[col] = np.where(izq, (out[col] + 180) % 360, out[col])
    return out

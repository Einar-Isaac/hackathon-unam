"""Distancias entre pass rushers y QB, frame a frame."""
import numpy as np
import pandas as pd


def distancias_rusher_qb(ventana: pd.DataFrame) -> pd.DataFrame:
    """Una fila por (rusher, frame) con `dist` al QB. Vacío si falta QB o rushers."""
    rol = ventana["pff_role"].str.lower()
    qb = ventana.loc[rol == "pass", ["frameId", "x", "y"]]
    rush = ventana.loc[rol == "pass rush", ["nflId", "frameId", "x", "y"]]
    if qb.empty or rush.empty:
        return pd.DataFrame(columns=["nflId", "frameId", "dist"])
    # validate asegura un solo QB por frame (no se duplican filas de rushers)
    j = rush.merge(qb, on="frameId", suffixes=("", "_qb"), validate="m:1")
    j["dist"] = np.hypot(j["x"] - j["x_qb"], j["y"] - j["y_qb"])
    return j[["nflId", "frameId", "dist"]]

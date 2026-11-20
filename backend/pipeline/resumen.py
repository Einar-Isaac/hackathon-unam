"""Tabla `metadatos`: conteos globales del conjunto de datos."""
import pandas as pd


def construir_metadatos(plays: pd.DataFrame, jm: pd.DataFrame, sin_snap: int) -> pd.DataFrame:
    """Una fila con dropbacks totales, partidos y jugadas analizadas."""
    return pd.DataFrame([{
        "n_dropbacks": len(plays),
        "n_partidos": int(plays["gameId"].nunique()),
        "n_analizadas": len(jm),
        "n_sin_snap": sin_snap,
    }])

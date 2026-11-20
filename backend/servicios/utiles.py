"""Utilidades de serialización."""
import pandas as pd

SHELLS = {0: "0-High (sin safeties profundos)", 1: "1-High (single high)", 2: "2-High (dos profundos)"}


def a_registros(df: pd.DataFrame) -> list[dict]:
    """DataFrame -> lista de dicts con NaN convertido a None (JSON válido)."""
    return df.astype(object).where(df.notna(), None).to_dict("records")


def etiqueta_shell(n_safeties: float | None) -> str | None:
    """Nombre del shell según safeties profundos al snap."""
    if n_safeties is None or pd.isna(n_safeties):
        return None
    return SHELLS.get(int(n_safeties), f"{int(n_safeties)} profundos")

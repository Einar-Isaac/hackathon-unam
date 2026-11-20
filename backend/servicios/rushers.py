"""Ranking de pass rushers más letales."""
from backend import repositorio
from backend.servicios.utiles import a_registros

COLUMNAS = ["nflId", "displayName", "officialPosition", "rush_snaps", "rupturas",
            "pct_ruptura", "seg_prom_colapso", "hits", "hurries", "sacks"]


def top_rushers(min_snaps: int, limite: int) -> list[dict]:
    """Top por tasa de ruptura < 2 yd, con mínimo de rush snaps."""
    df = repositorio.ranking_rushers(min_snaps, limite)[COLUMNAS]
    for c in ("hits", "hurries", "sacks"):
        df[c] = df[c].astype(int)
    return a_registros(df)

"""Letalidad por pass rusher: tasa de ruptura (< 2 yd del QB) y presión PFF."""
import pandas as pd

from backend.pipeline.carga import unir_validado
from backend.pipeline.config import DIR_DATOS, DISTANCIA_ROMPE, SEG_POR_FRAME
from backend.pipeline.distancias import distancias_rusher_qb
from backend.pipeline.eventos import ventana_observada

COLS_CRUCES = ["gameId", "playId", "nflId", "roto", "tiempo_colapso"]


def cruces_por_rusher(jugada: pd.DataFrame, f_snap: int, f_fin: int, evento: str) -> pd.DataFrame:
    """Por cada rusher de la jugada: si llegó a < 2.0 yd del QB antes del pase y cuándo."""
    dist = distancias_rusher_qb(ventana_observada(jugada, f_snap, f_fin, evento))
    if dist.empty:
        return pd.DataFrame(columns=COLS_CRUCES)
    primer = dist[dist["dist"] < DISTANCIA_ROMPE].groupby("nflId")["frameId"].min()
    out = pd.DataFrame({"nflId": dist["nflId"].unique()})
    frame = out["nflId"].map(primer)
    out["roto"] = frame.notna().astype(int)
    out["tiempo_colapso"] = ((frame - f_snap) * SEG_POR_FRAME).round(1)
    out.insert(0, "playId", int(jugada["playId"].iloc[0]))
    out.insert(0, "gameId", int(jugada["gameId"].iloc[0]))
    out["nflId"] = out["nflId"].astype(int)
    return out[COLS_CRUCES]


def cargar_pff_presion() -> pd.DataFrame:
    """Hits, hurries y sacks por jugador y jugada (NA = 0 eventos)."""
    cols = ["gameId", "playId", "nflId", "pff_hit", "pff_hurry", "pff_sack"]
    pff = pd.read_csv(DIR_DATOS / "pffScoutingData.csv", usecols=cols)
    return pff.fillna({"pff_hit": 0, "pff_hurry": 0, "pff_sack": 0})


def agregar_rushers(cruces: pd.DataFrame, pff_presion: pd.DataFrame,
                    players: pd.DataFrame) -> pd.DataFrame:
    """Tabla por jugador: snaps, % ruptura, segundos promedio al colapso y H/G/S."""
    n = len(cruces)
    df = unir_validado(cruces, pff_presion, ["gameId", "playId", "nflId"], "rushers-pff")
    df = unir_validado(df, players[["nflId", "displayName", "officialPosition"]],
                       ["nflId"], "rushers-players")
    if len(df) != n:
        raise ValueError("agregar_rushers cambió el número de filas")

    g = df.groupby(["nflId", "displayName", "officialPosition"], dropna=False)
    ranking = g.agg(rush_snaps=("roto", "size"), rupturas=("roto", "sum"),
                    seg_prom_colapso=("tiempo_colapso", "mean"),
                    hits=("pff_hit", "sum"), hurries=("pff_hurry", "sum"),
                    sacks=("pff_sack", "sum")).reset_index()
    ranking["pct_ruptura"] = 100 * ranking["rupturas"] / ranking["rush_snaps"]
    return ranking.sort_values(["pct_ruptura", "rush_snaps"], ascending=False).reset_index(drop=True)

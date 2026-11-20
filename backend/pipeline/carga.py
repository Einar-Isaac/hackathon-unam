"""Extracción: lectura de CSV y unión validada con tablas de contexto."""
from pathlib import Path

import pandas as pd

from backend.pipeline.config import DIR_DATOS
from backend.pipeline.normalizacion import normalizar_direccion

COLS_TRACKING = ["gameId", "playId", "nflId", "frameId", "jerseyNumber", "team",
                 "playDirection", "x", "y", "s", "o", "dir", "event"]
COLS_PLAYS = ["gameId", "playId", "possessionTeam", "defensiveTeam", "passResult",
              "offenseFormation", "pff_passCoverage"]
COLS_PFF = ["gameId", "playId", "nflId", "pff_role", "pff_positionLinedUp"]
COLS_PLAYERS = ["nflId", "officialPosition", "displayName"]


def unir_validado(izq: pd.DataFrame, der: pd.DataFrame, llaves: list[str],
                  nombre: str) -> pd.DataFrame:
    """Left merge muchos-a-uno; falla si se duplican o pierden filas."""
    n_antes = len(izq)
    # validate lanza MergeError si 'der' repite llaves (duplicaría filas)
    out = izq.merge(der, on=llaves, how="left", validate="m:1")
    if len(out) != n_antes:
        raise ValueError(f"Merge {nombre}: {n_antes} filas -> {len(out)}")
    return out


def cargar_tablas_base() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Lee plays, pffScoutingData y players (solo columnas necesarias)."""
    plays = pd.read_csv(DIR_DATOS / "plays.csv", usecols=COLS_PLAYS)
    pff = pd.read_csv(DIR_DATOS / "pffScoutingData.csv", usecols=COLS_PFF)
    players = pd.read_csv(DIR_DATOS / "players.csv", usecols=COLS_PLAYERS)
    if plays.duplicated(["gameId", "playId"]).any():
        raise ValueError("plays.csv tiene (gameId, playId) duplicados")
    return plays, pff, players


def listar_tracking() -> list[Path]:
    """Archivos tracking_*.csv ordenados."""
    archivos = sorted(DIR_DATOS.glob("tracking_*.csv"))
    if not archivos:
        raise FileNotFoundError(f"No hay tracking_*.csv en {DIR_DATOS}")
    return archivos


def cargar_tracking(ruta: Path, plays: pd.DataFrame, pff: pd.DataFrame,
                    players: pd.DataFrame) -> pd.DataFrame:
    """Lee un tracking, lo enriquece con contexto y lo normaliza espacialmente."""
    trk = pd.read_csv(ruta, usecols=COLS_TRACKING)
    n_inicial = len(trk)

    trk = unir_validado(trk, plays, ["gameId", "playId"], "tracking-plays")
    if trk["defensiveTeam"].isna().any():
        raise ValueError(f"{ruta.name}: jugadas de tracking ausentes en plays.csv")

    trk = unir_validado(trk, pff, ["gameId", "playId", "nflId"], "tracking-pff")
    trk = unir_validado(trk, players, ["nflId"], "tracking-players")
    if len(trk) != n_inicial:
        raise ValueError(f"{ruta.name}: cambió el número de filas tras los merges")
    return normalizar_direccion(trk)

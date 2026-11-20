"""Acceso de solo lectura a data/pocket.db (solo SQL, sin lógica de negocio)."""
import sqlite3
from contextlib import closing

import pandas as pd

from backend.pipeline.config import RUTA_DB


def _consulta(sql: str, params: tuple = ()) -> pd.DataFrame:
    """Ejecuta una consulta parametrizada y devuelve un DataFrame."""
    with closing(sqlite3.connect(f"file:{RUTA_DB.as_posix()}?mode=ro", uri=True)) as con:
        return pd.read_sql_query(sql, con, params=params)


def jugadas_metricas() -> pd.DataFrame:
    return _consulta("SELECT * FROM jugadas_metricas")


def ranking() -> pd.DataFrame:
    return _consulta("SELECT * FROM ranking_defensas_disguise ORDER BY disguise_score_prom DESC")


def curvas(variable: str) -> pd.DataFrame:
    return _consulta("SELECT * FROM curvas_supervivencia WHERE variable = ? "
                     "ORDER BY grupo, tiempo_s", (variable,))


def catalogo_muestra() -> pd.DataFrame:
    """Las jugadas de la muestra con sus métricas."""
    return _consulta(
        "SELECT m.* FROM jugadas_metricas m JOIN "
        "(SELECT DISTINCT gameId, playId, tipo_muestra FROM tracking_muestra) s "
        "ON m.gameId = s.gameId AND m.playId = s.playId")


def tipo_muestra() -> pd.DataFrame:
    return _consulta("SELECT DISTINCT gameId, playId, tipo_muestra FROM tracking_muestra")


def frames_jugada(game_id: int, play_id: int) -> pd.DataFrame:
    return _consulta("SELECT * FROM tracking_muestra WHERE gameId = ? AND playId = ? "
                     "ORDER BY frameId, nflId", (game_id, play_id))


def metricas_jugada(game_id: int, play_id: int) -> pd.DataFrame:
    return _consulta("SELECT * FROM jugadas_metricas WHERE gameId = ? AND playId = ?",
                     (game_id, play_id))

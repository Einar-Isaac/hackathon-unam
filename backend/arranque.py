"""Garantiza que data/pocket.db exista al arrancar (servidor efímero)."""
import sqlite3
from contextlib import closing
from pathlib import Path

from backend.pipeline.config import RUTA_DB
from backend.pipeline.verificacion import TABLAS


def _tablas_existentes(ruta: Path) -> set[str]:
    with closing(sqlite3.connect(ruta)) as con:
        filas = con.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    return {f[0] for f in filas}


def asegurar_db(ruta: Path = RUTA_DB) -> bool:
    """Ejecuta el ETL si falta la base o sus tablas. Devuelve True si lo ejecutó."""
    if ruta.exists() and set(TABLAS) <= _tablas_existentes(ruta):
        return False
    from backend.etl import ejecutar  # import diferido: el ETL es pesado
    print("pocket.db ausente o incompleta: ejecutando ETL (varios minutos)...", flush=True)
    ejecutar()
    return True

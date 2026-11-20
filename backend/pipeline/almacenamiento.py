"""Persistencia en SQLite (biblioteca estándar, sin dependencias nuevas)."""
import sqlite3
from contextlib import closing
from pathlib import Path

import pandas as pd


def guardar_tablas(tablas: dict[str, pd.DataFrame], ruta_db: Path) -> None:
    """Escribe cada DataFrame como tabla, reemplazando versiones previas."""
    ruta_db.parent.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(ruta_db)) as con:
        for nombre, df in tablas.items():
            df.to_sql(nombre, con, if_exists="replace", index=False)
        con.commit()


def leer_tabla(ruta_db: Path, nombre: str) -> pd.DataFrame:
    """Lee una tabla completa desde la base."""
    with closing(sqlite3.connect(ruta_db)) as con:
        return pd.read_sql_query(f"SELECT * FROM {nombre}", con)  # nombre fijo interno

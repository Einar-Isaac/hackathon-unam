"""Reporte de verificación sobre la base ya escrita (shape, nulos, S(2.5 s))."""
from pathlib import Path

import pandas as pd

from backend.pipeline.almacenamiento import leer_tabla

TABLAS = ["jugadas_metricas", "curvas_supervivencia",
          "ranking_defensas_disguise", "tracking_muestra",
          "ranking_pass_rushers", "metadatos"]


def reporte(ruta_db: Path, sin_snap: int) -> None:
    """Imprime shape, nulos por columna y supervivencia a 2.5 s por cobertura."""
    print("\n=== SHAPE Y NULOS POR TABLA ===")
    for nombre in TABLAS:
        df = leer_tabla(ruta_db, nombre)
        nulos = df.isna().sum()
        print(f"\n[{nombre}] shape={df.shape}")
        print("  nulos:", nulos[nulos > 0].to_dict() or "ninguno")

    jm = leer_tabla(ruta_db, "jugadas_metricas")
    print(f"\nJugadas sin evento de snap (excluidas): {sin_snap}")
    print("disguise_score:\n", jm["disguise_score"].describe().round(2).to_string())
    print("bolsillo_roto:", jm["bolsillo_roto"].value_counts(dropna=False).to_dict())
    print("tiempo_observado:\n", jm["tiempo_observado"].describe().round(2).to_string())

    curvas = leer_tabla(ruta_db, "curvas_supervivencia")
    s25 = curvas[(curvas["variable"] == "pff_passCoverage") & (curvas["tiempo_s"] == 2.5)]
    s25 = s25[["grupo", "supervivencia", "n_en_riesgo", "n_jugadas"]]
    print("\n=== P(bolsillo sobrevive) a 2.5 s por cobertura ===")
    print(s25.sort_values("supervivencia").round(3).to_string(index=False))

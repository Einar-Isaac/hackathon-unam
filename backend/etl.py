"""Orquestador ETL. Ejecuta desde la raíz: .venv\\Scripts\\python.exe -m backend.etl"""
import sys

import pandas as pd

from backend.pipeline.almacenamiento import guardar_tablas
from backend.pipeline.carga import cargar_tablas_base
from backend.pipeline.config import RUTA_DB
from backend.pipeline.kaplan_meier import curvas_por_grupo
from backend.pipeline.metricas import construir_jugadas_metricas
from backend.pipeline.muestra import extraer_muestra, seleccionar_jugadas
from backend.pipeline.rankings import ranking_defensas
from backend.pipeline.verificacion import reporte


def ejecutar() -> int:
    """Corre el pipeline completo y guarda las 4 tablas. Devuelve jugadas sin snap."""
    plays, pff, players = cargar_tablas_base()
    print("1/4 Métricas por jugada...")
    jm, sin_snap = construir_jugadas_metricas(plays, pff, players)

    print("2/4 Curvas Kaplan-Meier...")
    curvas = pd.concat([curvas_por_grupo(jm, "pff_passCoverage"),
                        curvas_por_grupo(jm, "offenseFormation")], ignore_index=True)

    print("3/4 Ranking de defensas...")
    ranking = ranking_defensas(jm)

    print("4/4 Muestra de tracking...")
    muestra = extraer_muestra(seleccionar_jugadas(jm), plays, pff, players)

    guardar_tablas({"jugadas_metricas": jm, "curvas_supervivencia": curvas,
                    "ranking_defensas_disguise": ranking, "tracking_muestra": muestra}, RUTA_DB)
    return sin_snap


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    reporte(RUTA_DB, ejecutar())

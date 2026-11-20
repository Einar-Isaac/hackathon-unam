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
from backend.pipeline.resumen import construir_metadatos
from backend.pipeline.rushers import agregar_rushers, cargar_pff_presion
from backend.pipeline.verificacion import reporte


def ejecutar() -> int:
    """Corre el pipeline completo y guarda las tablas. Devuelve jugadas sin snap."""
    plays, pff, players = cargar_tablas_base()
    print("1/5 Métricas por jugada y por rusher...")
    jm, cruces, sin_snap = construir_jugadas_metricas(plays, pff, players)

    print("2/5 Curvas Kaplan-Meier...")
    curvas = pd.concat([curvas_por_grupo(jm, "pff_passCoverage"),
                        curvas_por_grupo(jm, "offenseFormation")], ignore_index=True)

    print("3/5 Ranking de defensas y pass rushers...")
    ranking = ranking_defensas(jm)
    rushers = agregar_rushers(cruces, cargar_pff_presion(), players)

    print("4/5 Muestra de tracking...")
    muestra = extraer_muestra(seleccionar_jugadas(jm), plays, pff, players)

    print("5/5 Guardando...")
    guardar_tablas({"jugadas_metricas": jm, "curvas_supervivencia": curvas,
                    "ranking_defensas_disguise": ranking, "tracking_muestra": muestra,
                    "ranking_pass_rushers": rushers,
                    "metadatos": construir_metadatos(plays, jm, sin_snap)}, RUTA_DB)
    return sin_snap


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    reporte(RUTA_DB, ejecutar())

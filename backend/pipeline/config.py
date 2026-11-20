"""Constantes del pipeline: rutas relativas al proyecto y parámetros de las métricas."""
from pathlib import Path

# Rutas relativas a la raíz del proyecto (no dependen del directorio de trabajo)
RAIZ = Path(__file__).resolve().parents[2]
DIR_DATOS = RAIZ / "data"
RUTA_DB = DIR_DATOS / "pocket.db"

RANDOM_STATE = 42

# Campo (yardas)
LARGO_CAMPO = 120.0
ANCHO_CAMPO = 53.3

# Eventos de tracking
EVENTOS_SNAP = ("ball_snap", "autoevent_ballsnap")
EVENTOS_PASE = ("pass_forward", "autoevent_passforward")
EVENTOS_SACK = ("qb_sack", "qb_strip_sack")
EVENTOS_FIN = EVENTOS_PASE + EVENTOS_SACK

# Disguise: safeties en caparazón profundo
POSICIONES_SAFETY = ("FS", "SS")
PROFUNDIDAD_MIN = 8.0
Y_MIN_PROFUNDO = 12.0
Y_MAX_PROFUNDO = 41.3
SAFETIES_ESPERADOS: dict[str, int] = {
    "Cover-0": 0,
    "Cover-1": 1,
    "Cover-3": 1,
    "Cover-2": 2,
    "2-Man": 2,
    "Quarters": 2,
    "Cover-6": 2,
}
PUNTOS_DESAJUSTE = 60.0
PUNTOS_MAX_MOVIMIENTO = 40.0
FACTOR_MOVIMIENTO = 8.0
FRAMES_1S = 10
UMBRAL_DISGUISE = 60.0
RESULTADOS_EXITO = ("I", "IN", "S")

# Supervivencia del bolsillo
SEG_POR_FRAME = 0.1
DISTANCIA_ROMPE = 2.0
T_MAX_KM = 4.5

# Muestra para animación
N_MUESTRA_DISGUISE = 15
N_MUESTRA_RUPTURA = 15
T_MIN_RUPTURA_MUESTRA = 0.5

"""Construye jugadas_metricas: una fila por (gameId, playId)."""
import pandas as pd

from backend.pipeline.bolsillo import calcular_bolsillo
from backend.pipeline.carga import cargar_tracking, listar_tracking
from backend.pipeline.disguise import calcular_disguise
from backend.pipeline.eventos import frame_fin, frame_snap

COLS_CONTEXTO = ["defensiveTeam", "possessionTeam", "pff_passCoverage",
                 "offenseFormation", "passResult"]


def metricas_de_jugada(jugada: pd.DataFrame) -> dict | None:
    """Métricas de una jugada normalizada; None si no tiene evento de snap."""
    f_snap = frame_snap(jugada)
    if f_snap is None:
        return None
    f_fin, evento = frame_fin(jugada, f_snap)
    primera = jugada.iloc[0]
    fila = {"gameId": int(primera["gameId"]), "playId": int(primera["playId"])}
    fila.update({c: primera[c] for c in COLS_CONTEXTO})
    fila.update(calcular_disguise(jugada, f_snap, primera["pff_passCoverage"]))
    fila.update(calcular_bolsillo(jugada, f_snap, f_fin, evento))
    fila.update({"frame_snap": f_snap, "frame_fin": f_fin, "evento_fin": evento})
    return fila


def construir_jugadas_metricas(plays: pd.DataFrame, pff: pd.DataFrame,
                               players: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """Recorre todos los tracking. Devuelve la tabla y el número de jugadas sin snap."""
    filas, sin_snap = [], 0
    archivos = listar_tracking()
    for i, ruta in enumerate(archivos, 1):
        trk = cargar_tracking(ruta, plays, pff, players)
        for _, jugada in trk.groupby(["gameId", "playId"], sort=False):
            fila = metricas_de_jugada(jugada)
            if fila is None:
                sin_snap += 1
            else:
                filas.append(fila)
        if i % 20 == 0 or i == len(archivos):
            print(f"  tracking procesados: {i}/{len(archivos)}", flush=True)

    jm = pd.DataFrame(filas)
    if jm.duplicated(["gameId", "playId"]).any():
        raise ValueError("jugadas_metricas tiene (gameId, playId) duplicados")
    return jm, sin_snap

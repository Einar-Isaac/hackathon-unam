"""Construye jugadas_metricas (una fila por jugada) y los cruces por pass rusher."""
import pandas as pd

from backend.pipeline.bolsillo import calcular_bolsillo
from backend.pipeline.carga import cargar_tracking, listar_tracking
from backend.pipeline.disguise import calcular_disguise
from backend.pipeline.eventos import frame_fin, frame_snap
from backend.pipeline.rushers import cruces_por_rusher

COLS_CONTEXTO = ["defensiveTeam", "possessionTeam", "pff_passCoverage",
                 "offenseFormation", "passResult"]


def metricas_de_jugada(jugada: pd.DataFrame) -> tuple[dict, pd.DataFrame] | None:
    """Métricas y cruces por rusher de una jugada normalizada; None si no tiene snap."""
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
    return fila, cruces_por_rusher(jugada, f_snap, f_fin, evento)


def construir_jugadas_metricas(plays: pd.DataFrame, pff: pd.DataFrame, players: pd.DataFrame
                               ) -> tuple[pd.DataFrame, pd.DataFrame, int]:
    """Recorre todos los tracking. Devuelve jugadas, cruces por rusher y jugadas sin snap."""
    filas, cruces, sin_snap = [], [], 0
    archivos = listar_tracking()
    for i, ruta in enumerate(archivos, 1):
        trk = cargar_tracking(ruta, plays, pff, players)
        for _, jugada in trk.groupby(["gameId", "playId"], sort=False):
            res = metricas_de_jugada(jugada)
            if res is None:
                sin_snap += 1
            else:
                filas.append(res[0])
                cruces.append(res[1])
        if i % 20 == 0 or i == len(archivos):
            print(f"  tracking procesados: {i}/{len(archivos)}", flush=True)

    jm = pd.DataFrame(filas)
    if jm.duplicated(["gameId", "playId"]).any():
        raise ValueError("jugadas_metricas tiene (gameId, playId) duplicados")
    # Se omiten jugadas sin QB/rushers (DataFrames vacíos) para no alterar los dtypes
    cruces_df = pd.concat([c for c in cruces if not c.empty], ignore_index=True)
    if cruces_df.duplicated(["gameId", "playId", "nflId"]).any():
        raise ValueError("cruces por rusher duplicados")
    return jm, cruces_df, sin_snap

"""tracking_muestra: frames normalizados de 30 jugadas representativas."""
import pandas as pd

from backend.pipeline.carga import cargar_tracking
from backend.pipeline.config import (
    DIR_DATOS, N_MUESTRA_DISGUISE, N_MUESTRA_RUPTURA, RANDOM_STATE, T_MIN_RUPTURA_MUESTRA,
)

COLS_SALIDA = ["gameId", "playId", "tipo_muestra", "frameId", "frame_rel_snap", "nflId",
               "displayName", "jerseyNumber", "team", "rol_equipo", "pff_role",
               "pff_positionLinedUp", "x", "y", "s", "o", "dir", "event"]


def seleccionar_jugadas(jm: pd.DataFrame) -> pd.DataFrame:
    """15 jugadas con mayor disguise y 15 con ruptura de bolsillo más rápida."""
    base = jm.dropna(subset=["disguise_score", "tiempo_observado"])
    altos = (base.sort_values(["disguise_score", "gameId", "playId"], ascending=[False, True, True])
             .head(N_MUESTRA_DISGUISE).assign(tipo_muestra="alto_disguise"))

    rotas = base[(base["bolsillo_roto"] == 1) & (base["tiempo_observado"] >= T_MIN_RUPTURA_MUESTRA)]
    rotas = rotas.drop(altos.index, errors="ignore")
    # Mezcla reproducible antes de ordenar para desempatar al azar (random_state=42)
    rotas = (rotas.sample(frac=1, random_state=RANDOM_STATE)
             .sort_values("tiempo_observado", kind="stable")
             .head(N_MUESTRA_RUPTURA).assign(tipo_muestra="ruptura_rapida"))
    sel = pd.concat([altos, rotas])
    if len(sel) != N_MUESTRA_DISGUISE + N_MUESTRA_RUPTURA:
        raise ValueError(f"Muestra incompleta: {len(sel)} jugadas")
    return sel[["gameId", "playId", "tipo_muestra", "frame_snap"]]


def extraer_muestra(sel: pd.DataFrame, plays: pd.DataFrame, pff: pd.DataFrame,
                    players: pd.DataFrame) -> pd.DataFrame:
    """Relee solo los juegos necesarios y devuelve todos los frames de cada jugada."""
    partes = []
    for gid, juego_sel in sel.groupby("gameId"):
        ruta = DIR_DATOS / f"tracking_{gid}.csv"
        trk = cargar_tracking(ruta, plays, pff, players)
        # merge validado: cada jugada elegida debe existir una sola vez en la muestra
        m = trk.merge(juego_sel, on=["gameId", "playId"], how="inner", validate="m:1")
        partes.append(m)
    muestra = pd.concat(partes, ignore_index=True)

    muestra["frame_rel_snap"] = muestra["frameId"] - muestra["frame_snap"]
    muestra["rol_equipo"] = "defensiva"
    muestra.loc[muestra["team"] == muestra["possessionTeam"], "rol_equipo"] = "ofensiva"
    muestra.loc[muestra["team"] == "football", "rol_equipo"] = "balon"
    muestra = muestra.sort_values(["gameId", "playId", "frameId", "nflId"])
    return muestra[COLS_SALIDA].reset_index(drop=True)

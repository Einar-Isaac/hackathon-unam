"""Catálogo de jugadas muestra y construcción de frames para el visor 2D."""
import numpy as np
import pandas as pd

from backend import repositorio
from backend.pipeline.config import POSICIONES_SAFETY, SEG_POR_FRAME
from backend.servicios.utiles import a_registros, etiqueta_shell

COLS_CATALOGO = ["gameId", "playId", "tipo_muestra", "defensiveTeam", "possessionTeam",
                 "pff_passCoverage", "offenseFormation", "passResult", "disguise_score",
                 "safeties_snap", "safeties_esperados", "tiempo_observado", "bolsillo_roto"]


def catalogo() -> list[dict]:
    """Las 30 jugadas de la muestra con su shell al snap vs. cobertura real."""
    df = repositorio.catalogo_muestra().merge(
        repositorio.tipo_muestra(), on=["gameId", "playId"], validate="1:1")
    df["shell_snap"] = df["safeties_snap"].map(etiqueta_shell)
    df = df.sort_values(["tipo_muestra", "disguise_score"], ascending=[True, False])
    return a_registros(df[COLS_CATALOGO + ["shell_snap"]])


def _asignar_rol(df: pd.DataFrame) -> pd.Series:
    """Rol visual: balon, qb, pass_rusher, safety, ofensiva o defensiva."""
    pos = df["pff_positionLinedUp"].fillna("").str.startswith(POSICIONES_SAFETY)
    condiciones = [df["rol_equipo"] == "balon", df["pff_role"] == "Pass",
                   df["pff_role"] == "Pass Rush", (df["rol_equipo"] == "defensiva") & pos]
    return pd.Series(np.select(condiciones, ["balon", "qb", "pass_rusher", "safety"],
                               default=df["rol_equipo"]), index=df.index)


def _frames(df: pd.DataFrame) -> list[dict]:
    """Agrupa filas por frame con la lista de jugadores redondeada."""
    df = df.assign(rol=_asignar_rol(df))
    campos = ["nflId", "displayName", "jerseyNumber", "rol", "pff_positionLinedUp", "x", "y", "o"]
    frames = []
    for rel, g in df.groupby("frame_rel_snap", sort=True):
        jug = a_registros(g[campos].round({"x": 2, "y": 2, "o": 1}))
        frames.append({"frame_rel": int(rel), "tiempo_s": round(rel * SEG_POR_FRAME, 1),
                       "evento": next((e for e in g["event"] if pd.notna(e)), None),
                       "jugadores": [{"id": j["nflId"], "nombre": j["displayName"],
                                      "camiseta": j["jerseyNumber"], "rol": j["rol"],
                                      "posicion": j["pff_positionLinedUp"],
                                      "x": j["x"], "y": j["y"], "o": j["o"]} for j in jug]})
    return frames


def detalle(game_id: int, play_id: int) -> dict | None:
    """Frames normalizados + métricas de la jugada; None si no está en la muestra."""
    frames = repositorio.frames_jugada(game_id, play_id)
    metricas = repositorio.metricas_jugada(game_id, play_id)
    if frames.empty or metricas.empty:
        return None
    m = a_registros(metricas)[0]
    roto = m["bolsillo_roto"] == 1
    return {
        "gameId": game_id, "playId": play_id,
        "tipo_muestra": frames["tipo_muestra"].iloc[0],
        "defensiveTeam": m["defensiveTeam"], "possessionTeam": m["possessionTeam"],
        "pff_passCoverage": m["pff_passCoverage"], "offenseFormation": m["offenseFormation"],
        "passResult": m["passResult"], "disguise_score": m["disguise_score"],
        "safeties_snap": m["safeties_snap"], "safeties_esperados": m["safeties_esperados"],
        "shell_snap": etiqueta_shell(m["safeties_snap"]),
        "bolsillo_roto": bool(roto), "tiempo_observado": m["tiempo_observado"],
        "frame_ruptura_rel": int(round(m["tiempo_observado"] / SEG_POR_FRAME)) if roto else None,
        "frame_fin_rel": int(m["frame_fin"] - m["frame_snap"]), "evento_fin": m["evento_fin"],
        "frames": _frames(frames),
    }

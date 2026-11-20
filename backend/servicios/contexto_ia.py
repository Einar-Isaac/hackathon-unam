"""Arma el contexto táctico (métricas reales de pocket.db) que recibe el analista IA."""
import pandas as pd

from backend import repositorio
from backend.pipeline.config import UMBRAL_DISGUISE
from backend.servicios.kpis import kpi_engano, kpi_ruptura, kpi_supervivencia
from backend.servicios.utiles import a_registros, etiqueta_shell

CAMPOS_JUGADA = ["gameId", "playId", "defensiveTeam", "possessionTeam", "pff_passCoverage",
                 "offenseFormation", "passResult", "disguise_score", "safeties_snap",
                 "safeties_esperados", "desplazamiento_safeties_1s", "tiempo_observado",
                 "bolsillo_roto", "evento_fin"]


def _contexto_jugada(game_id: int, play_id: int) -> dict | None:
    df = repositorio.metricas_jugada(game_id, play_id)
    if df.empty:
        return None
    m = a_registros(df[CAMPOS_JUGADA])[0]
    m["shell_snap"] = etiqueta_shell(m["safeties_snap"])
    m["bolsillo_roto"] = bool(m["bolsillo_roto"] == 1)
    m["engano_detectado"] = m["disguise_score"] is not None and m["disguise_score"] >= UMBRAL_DISGUISE
    m["tipo"] = "jugada"
    m["insignias"] = {"disguise": m["disguise_score"], "ttb_s": m["tiempo_observado"],
                      "ttb_roto": m["bolsillo_roto"], "cobertura": m["pff_passCoverage"],
                      "shell": m["shell_snap"]}
    return m


def _contexto_agregado(jm: pd.DataFrame, cobertura: str | None) -> dict:
    """Métricas de un conjunto de jugadas (una cobertura o todas)."""
    sup, eng, rup = kpi_supervivencia(jm), kpi_engano(jm), kpi_ruptura(jm)
    disguise = jm["disguise_score"].dropna()
    ctx = {"tipo": "cobertura" if cobertura else "global", "cobertura": cobertura,
           "n_jugadas": int(len(jm)),
           "disguise_promedio": float(disguise.mean()) if len(disguise) else None,
           "pct_disfrazadas": float(100 * (disguise >= UMBRAL_DISGUISE).mean()) if len(disguise) else None}
    ctx.update(sup)
    ctx.update(eng)
    ctx.update({k: rup[k] for k in ("pct_ruptura", "pct_sack_con_colapso", "pct_sack_sin_colapso")})
    ctx["insignias"] = {"disguise": ctx["disguise_promedio"], "ttb_s": sup["mediana_colapso_s"],
                        "ttb_roto": None, "cobertura": cobertura or "Todas", "shell": None}
    return ctx


def construir_contexto(game_id: int | None, play_id: int | None, cobertura: str | None) -> dict | None:
    """Contexto de una jugada, de una cobertura o global. None si no existe en la base."""
    if game_id is not None and play_id is not None:
        return _contexto_jugada(game_id, play_id)
    jm = repositorio.jugadas_metricas()
    if cobertura:
        jm = jm[jm["pff_passCoverage"] == cobertura]
        if jm.empty:
            return None
    return _contexto_agregado(jm, cobertura)

"""Endpoints /api: overview, supervivencia, jugadas, pass rushers y análisis IA."""
from typing import Literal

from fastapi import APIRouter, HTTPException, Query

from backend.api.esquemas import SolicitudAnalisis
from backend.servicios import (
    analista_ia, contexto_ia, jugadas, kpis, rushers, supervivencia,
)

router = APIRouter(prefix="/api")


@router.get("/overview")
def overview() -> dict:
    """KPIs globales y ranking de defensas por disguise."""
    return kpis.calcular_overview()


@router.get("/pass-rushers")
def pass_rushers(min_snaps: int = Query(40, ge=1), limite: int = Query(8, ge=1, le=50)) -> list[dict]:
    """Pass rushers con mayor tasa de ruptura (< 2 yd del QB)."""
    return rushers.top_rushers(min_snaps, limite)


@router.get("/supervivencia")
def curvas_supervivencia(
    agrupar_por: Literal["pff_passCoverage", "offenseFormation"] = "pff_passCoverage",
) -> dict:
    """Curvas Kaplan-Meier por cobertura o formación."""
    return supervivencia.series(agrupar_por)


@router.get("/jugadas")
def catalogo_jugadas() -> list[dict]:
    """Catálogo de las jugadas muestra."""
    return jugadas.catalogo()


@router.get("/jugadas/{game_id}/{play_id}")
def detalle_jugada(game_id: int, play_id: int) -> dict:
    """Frames normalizados y métricas de una jugada de la muestra."""
    d = jugadas.detalle(game_id, play_id)
    if d is None:
        raise HTTPException(status_code=404, detail="Jugada fuera de la muestra")
    return d


@router.post("/analisis-ia")
def analisis_ia(solicitud: SolicitudAnalisis) -> dict:
    """Análisis táctico con Amazon Nova (o diagnóstico offline si AWS no responde)."""
    contexto = contexto_ia.construir_contexto(solicitud.game_id, solicitud.play_id, solicitud.cobertura)
    if contexto is None:
        raise HTTPException(status_code=404, detail="Jugada o cobertura no encontrada")
    resultado = analista_ia.analizar(contexto, solicitud.pregunta)
    return {**resultado, "contexto": contexto}

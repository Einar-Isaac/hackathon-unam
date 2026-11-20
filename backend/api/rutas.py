"""Endpoints /api: overview, supervivencia y jugadas."""
from typing import Literal

from fastapi import APIRouter, HTTPException, Query

from backend.servicios import jugadas, kpis, rushers, supervivencia

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


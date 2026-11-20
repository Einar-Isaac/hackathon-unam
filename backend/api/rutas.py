"""Endpoints /api: overview, supervivencia y jugadas."""
from typing import Literal

from fastapi import APIRouter, HTTPException

from backend.servicios import jugadas, kpis, supervivencia

router = APIRouter(prefix="/api")


@router.get("/overview")
def overview() -> dict:
    """KPIs globales y ranking de defensas por disguise."""
    return kpis.calcular_overview()


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

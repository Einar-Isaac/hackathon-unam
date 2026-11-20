"""API FastAPI. Ejecuta: python -m uvicorn backend.main:app --port 8000"""
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.api.rutas import router
from backend.arranque import asegurar_db

DIST = Path(__file__).resolve().parent.parent / "dashboard" / "dist"


@asynccontextmanager
async def lifespan(_: FastAPI):
    asegurar_db()  # si falta pocket.db, regenera con el ETL
    yield


app = FastAPI(title="Hackathon NFL UNAM", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["GET"],
                   allow_headers=["*"])


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


app.include_router(router)

# Sirve el build del dashboard en la misma URL (debe ir al final)
if DIST.is_dir():
    app.mount("/", StaticFiles(directory=DIST, html=True), name="dashboard")

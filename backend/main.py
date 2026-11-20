"""API FastAPI. Ejecuta: python -m uvicorn backend.main:app --port 8000"""
import os
from contextlib import asynccontextmanager
from pathlib import Path


def cargar_env():
    f = Path(__file__).resolve().parent.parent / ".env"
    if f.exists():
        for linea in f.read_text(encoding="utf-8-sig").splitlines():
            linea = linea.strip()
            if linea and not linea.startswith("#") and "=" in linea:
                k, v = linea.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


cargar_env()  # antes de usar boto3 (las llaves quedan solo en el entorno del proceso)

from fastapi import FastAPI  # noqa: E402
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402
from fastapi.staticfiles import StaticFiles  # noqa: E402

from backend.api.rutas import router  # noqa: E402
from backend.arranque import asegurar_db  # noqa: E402

DIST = Path(__file__).resolve().parent.parent / "dashboard" / "dist"


@asynccontextmanager
async def lifespan(_: FastAPI):
    asegurar_db()  # si falta pocket.db, regenera con el ETL
    yield


app = FastAPI(title="Hackathon NFL UNAM", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["GET", "POST"],
                   allow_headers=["*"])


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


app.include_router(router)

# Sirve el build del dashboard en la misma URL (debe ir al final)
if DIST.is_dir():
    app.mount("/", StaticFiles(directory=DIST, html=True), name="dashboard")

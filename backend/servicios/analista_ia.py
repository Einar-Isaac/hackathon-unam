"""Analista táctico: Amazon Nova en Bedrock (converse) con respaldo offline."""
import json
import logging
import os
from functools import lru_cache

import boto3
from botocore.exceptions import ClientError, EndpointConnectionError, NoCredentialsError

from backend.servicios.diagnostico_offline import diagnostico_offline

log = logging.getLogger(__name__)

PROMPT_SISTEMA = (
    "Actúa como Coordinador Ofensivo de la NFL. Analiza SOLO las métricas reales que recibes "
    "(disguise_score, shell al snap vs cobertura real pff_passCoverage, tiempo_observado hasta la "
    "ruptura del bolsillo < 2 yd, formación ofensiva y resultado). No inventes datos. "
    "Responde en español con un máximo de 4 viñetas accionables, cada una iniciada con «- »: "
    "(1) lectura del engaño de los safeties, (2) diagnóstico de la protección de la línea, "
    "(3) ajuste recomendado para el QB, y (4) opcional, respuesta breve a la pregunta del coach. "
    "Cada viñeta debe citar al menos una cifra del contexto. Si el contexto es agregado "
    "(cobertura o global), habla de tendencias y no de una sola jugada."
)


@lru_cache(maxsize=1)
def _cliente():
    """Cliente Bedrock solo con región; las credenciales las resuelve boto3 (rol o .env)."""
    region = os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client("bedrock-runtime", region_name=region)


def _modelo() -> str:
    return os.environ.get("BEDROCK_MODEL_ID", "us.amazon.nova-pro-v1:0")


def _consultar_nova(contexto: dict, pregunta: str | None) -> str:
    """Llama a Nova vía converse(); lanza las excepciones de boto3 sin tragarlas."""
    datos = {k: v for k, v in contexto.items() if k != "insignias"}
    texto = f"Contexto táctico (JSON):\n{json.dumps(datos, ensure_ascii=False, default=str)}"
    if pregunta:
        texto += f"\n\nPregunta del coach: {pregunta}"
    resp = _cliente().converse(
        modelId=_modelo(),
        system=[{"text": PROMPT_SISTEMA}],
        messages=[{"role": "user", "content": [{"text": texto}]}],
        inferenceConfig={"maxTokens": 600, "temperature": 0.3},
    )
    return resp["output"]["message"]["content"][0]["text"].strip()


def analizar(contexto: dict, pregunta: str | None) -> dict:
    """Devuelve {modo, modelo, analisis, aviso}. Cae a offline solo ante fallos de AWS."""
    try:
        return {"modo": "nova", "modelo": _modelo(),
                "analisis": _consultar_nova(contexto, pregunta), "aviso": None}
    except NoCredentialsError:
        aviso = "Sin credenciales de AWS en el entorno."
    except ClientError as e:  # credenciales expiradas, acceso denegado, modelo no disponible...
        aviso = f"Bedrock rechazó la llamada ({e.response['Error']['Code']})."
    except EndpointConnectionError:
        aviso = "No hay conexión con el endpoint de Bedrock."
    log.warning("Analista IA en modo offline: %s", aviso)
    return {"modo": "offline", "modelo": None,
            "analisis": diagnostico_offline(contexto, pregunta), "aviso": aviso}


def generar_analisis_tactico(contexto_jugada: dict, pregunta_usuario: str | None) -> str:
    """Texto del análisis táctico (Nova, o diagnóstico offline si AWS no está disponible)."""
    return analizar(contexto_jugada, pregunta_usuario)["analisis"]

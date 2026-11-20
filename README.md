# Pocket Intelligence · NFL Big Data Bowl 2026 UNAM

Construimos un tablero táctico que mide dos cosas con el tracking de 8,557 dropbacks de 122 partidos: cuánto disfrazan las defensas su cobertura antes del snap (Disguise Score, de 0 a 100) y cuánto tiempo sobrevive el bolsillo antes de que un pass rusher llegue a menos de 2 yardas del QB (curvas Kaplan-Meier). Los datos muestran que el bolsillo aguanta 87.4% de las jugadas hasta los 2.5 s, que cae a 79.8% contra Cover-0 y que la formación importa tanto como la cobertura (84.1% en I-Form contra 94.5% en Pistol). Cover-0 es además la cobertura más engañosa: solo la mitad de las veces muestra al snap el shell sin safeties profundos que le corresponde. El engaño no ayuda a todas las defensas por igual: en promedio la defensa falla 39.3% de las veces con engaño contra 40.9% sin él, pero equipos como LAC (41.7% contra 34.4%) sí lo convierten en ventaja. Está pensado para Coordinadores Ofensivos y Quarterbacks que quieren decidir cuándo acortar la progresión, cuándo reforzar la protección y cuánto confiar en lo que muestra la defensa antes del snap.

## Qué incluye

- **ETL** (`backend/etl.py`): normaliza el campo para que la ofensiva ataque siempre de izquierda a derecha y genera `data/pocket.db` con las métricas por jugada, las curvas de supervivencia, el ranking de defensas y de pass rushers, y una muestra de 30 jugadas para animación.
- **API** (FastAPI, bajo `/api`): KPIs, curvas de supervivencia, rankings y jugadas.
- **Dashboard** (React + TypeScript + Tailwind + Recharts): KPIs, curvas, rankings y un visor 2D de cancha con los safeties, el radio de 2 yd del QB y la comparación "Al snap parecía → Real".
- **Asistente táctico IA** (Amazon Nova en Bedrock): analiza la jugada o cobertura seleccionada. Si AWS no está disponible, entrega un diagnóstico offline con las mismas métricas.

## Cómo correrlo

```powershell
# Backend (si falta data/pocket.db, se regenera solo al arrancar con el ETL, ~2 min)
.\.venv\Scripts\python.exe -m uvicorn backend.main:app --port 8000

# Frontend: compilar y abrir http://127.0.0.1:8000
$env:PATH = "$((Resolve-Path .\.hackathon\.tools\node).Path);$env:PATH"
cd dashboard; npm run build

# Hallazgos para el pitch (solo lectura)
.\.venv\Scripts\python.exe -m backend.hallazgos
```

Para activar Nova, copia `.env.example` a `.env` y pega las llaves temporales de AWS. Sin llaves, la app funciona en modo offline.

## Definiciones

- **Disguise Score:** 60 puntos si los safeties profundos al snap no coinciden con los que pide la cobertura real, más hasta 40 puntos por el desplazamiento de los safeties en el primer segundo. Se considera engaño con 60 o más.
- **Ruptura del bolsillo:** un pass rusher llega a menos de 2.0 yd del QB antes del pase. Un sack cuenta como ruptura aunque no haya cruce previo.
- **Éxito del engaño:** la jugada disfrazada termina en incompleto, intercepción o sack.

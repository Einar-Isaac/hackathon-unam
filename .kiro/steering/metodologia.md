# Metodología obligatoria del proyecto

Estas reglas se aplican en CADA tarea de la sesión. Complementan `rules.md` (stack y despliegue) sin reemplazarlo.

## 1. Arquitectura modular (Specs-First)

- Nunca mezcles extracción de datos, procesamiento matemático, endpoints API e interfaz en un mismo archivo.
- Responsabilidad única por archivo y por función. Si un archivo supera las 250 líneas, divídelo en submódulos.
- Código simple y limpio, con *type hints*, *docstrings* concisos en las funciones principales y comentarios breves en español.

## 2. Bucle de retroalimentación obligatorio

- Nunca des una tarea por terminada sin ejecutar el código en la terminal e inspeccionar la salida real: `shape`, nulos (`NaN`), tipos de datos y coherencia lógica.
- Si hay errores o advertencias críticas, diagnostica la causa raíz y corrige antes de avanzar.

## 3. Guardrails estrictos

- Prohibido silenciar errores con `try / except: pass`.
- Cero rutas absolutas locales (`C:/...`) y cero secretos hardcodeados. Usa rutas relativas (`./data/...`) o `.env`.
- Reproducibilidad garantizada (`random_state=42`).
- Integridad de datos: en cada `merge` entre tablas valida explícitamente que no se dupliquen filas ni se pierdan registros clave.
- Si agregas una dependencia nueva, regístrala en el archivo de dependencias del proyecto (y recuerda que `rules.md` restringe el stack fijo).

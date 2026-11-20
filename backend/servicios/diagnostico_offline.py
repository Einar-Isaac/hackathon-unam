"""Diagnóstico táctico determinista (modo offline) con las métricas exactas de pocket.db."""

UMBRAL_PASE_S = 2.5


def _f(v: float | None, d: int = 1, sufijo: str = "") -> str:
    return "N/D" if v is None else f"{v:.{d}f}{sufijo}"


def _jugada(c: dict) -> list[str]:
    """Tres lecturas (engaño, protección, ajuste QB) de una jugada concreta."""
    ttb, roto = c["tiempo_observado"], c["bolsillo_roto"]
    if c["disguise_score"] is None:
        engano = (f"Engaño: la cobertura real ({c['pff_passCoverage']}) no tiene un shell esperado "
                  "definido, así que el Disguise Score no es evaluable.")
    elif c["engano_detectado"]:
        engano = (f"Engaño: al snap mostró {c['shell_snap']} ({_f(c['safeties_snap'], 0)} safeties profundos) "
                  f"pero la cobertura real fue {c['pff_passCoverage']} ({_f(c['safeties_esperados'], 0)} esperados). "
                  f"Disguise {_f(c['disguise_score'])}; los safeties se movieron "
                  f"{_f(c['desplazamiento_safeties_1s'], 2)} yd en 1 s.")
    else:
        engano = (f"Engaño: el shell {c['shell_snap']} coincide con {c['pff_passCoverage']}; "
                  f"Disguise {_f(c['disguise_score'])}, la lectura pre-snap era confiable.")

    if roto:
        sev = "antes del umbral de 2.5 s" if ttb is not None and ttb < UMBRAL_PASE_S else "después de 2.5 s"
        prot = f"Protección: el bolsillo se rompió (< 2 yd) a {_f(ttb)} s, {sev} ({c['evento_fin']})."
    else:
        prot = f"Protección: bolsillo intacto; el pase salió a {_f(ttb)} s sin que un rusher llegara a 2 yd."

    if roto and ttb is not None and ttb < UMBRAL_PASE_S:
        qb = "QB: acorta la progresión a lectura rápida (≤ 2.2 s), usa hot route o salida de ayuda a la protección."
    elif c["engano_detectado"]:
        qb = "QB: no te cases con el shell pre-snap; confirma la rotación de safeties post-snap antes de soltar."
    else:
        qb = "QB: hay ventana para la progresión completa; mantén el timing y la lectura del shell."
    return [engano, prot, qb]


def _agregado(c: dict) -> list[str]:
    """Tres lecturas para una cobertura o para el conjunto global."""
    nombre = c["cobertura"] or "todas las coberturas"
    return [
        f"Engaño ({nombre}, {c['n_jugadas']} jugadas): Disguise promedio {_f(c['disguise_promedio'])}; "
        f"{_f(c['pct_disfrazadas'], 1, '%')} de las jugadas se disfrazan (≥ 60). "
        f"Fallan {_f(c['pct_fallido_con_engano'], 1, '%')} con engaño vs {_f(c['pct_fallido_sin_engano'], 1, '%')} sin él.",
        f"Protección: el bolsillo sobrevive {_f(100 * c['supervivencia_2_5s'], 1, '%')} a 2.5 s; "
        f"se rompe en {_f(c['pct_ruptura'], 1, '%')} de las jugadas, con mediana de colapso en "
        f"{_f(c['mediana_colapso_s'], 1, ' s')}.",
        "QB: planea el timing alrededor de 2.5 s y reserva salidas rápidas para pre-snaps con shell engañoso.",
    ]


def diagnostico_offline(contexto: dict, pregunta: str | None) -> str:
    """Viñetas con las métricas exactas; indica que se generó en modo offline."""
    lineas = _jugada(contexto) if contexto["tipo"] == "jugada" else _agregado(contexto)
    if pregunta:
        lineas.append(f"Pregunta del coach: «{pregunta}». En modo offline no se responde en lenguaje libre; "
                      "usa las métricas anteriores o reintenta con Nova activo.")
    return "\n".join(f"- {linea}" for linea in lineas)

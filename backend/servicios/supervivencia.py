"""Series Kaplan-Meier listas para graficar."""
from backend import repositorio


def series(variable: str) -> dict:
    """Una serie (0.0-4.5 s) por grupo de `variable`."""
    df = repositorio.curvas(variable)
    grupos = []
    for grupo, g in df.groupby("grupo", sort=True):
        grupos.append({
            "grupo": grupo,
            "n_jugadas": int(g["n_jugadas"].iloc[0]),
            "puntos": [{"tiempo_s": float(r.tiempo_s), "supervivencia": float(r.supervivencia),
                        "n_en_riesgo": int(r.n_en_riesgo)} for r in g.itertuples()],
        })
    return {"agrupar_por": variable, "umbral_s": 2.5, "grupos": grupos}

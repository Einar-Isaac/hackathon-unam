"""Localiza frames clave (snap y fin de jugada) dentro de una jugada."""
import pandas as pd

from backend.pipeline.config import EVENTOS_FIN, EVENTOS_PASE, EVENTOS_SNAP


def frame_snap(jugada: pd.DataFrame) -> int | None:
    """Primer frame con evento de snap; None si la jugada no lo trae."""
    f = jugada.loc[jugada["event"].isin(EVENTOS_SNAP), "frameId"]
    return int(f.min()) if not f.empty else None


def frame_fin(jugada: pd.DataFrame, f_snap: int) -> tuple[int, str]:
    """Primer evento de fin (pase/sack) tras el snap; si no hay, el último frame."""
    fin = jugada[jugada["event"].isin(EVENTOS_FIN) & (jugada["frameId"] >= f_snap)]
    if fin.empty:
        return int(jugada["frameId"].max()), "ultimo_frame"
    fila = fin.sort_values("frameId").iloc[0]
    return int(fila["frameId"]), str(fila["event"])


def ventana_observada(jugada: pd.DataFrame, f_snap: int, f_fin: int, evento: str) -> pd.DataFrame:
    """Frames del snap al fin; en pases el frame del lanzamiento no cuenta (antes de lanzar)."""
    ultimo = f_fin - 1 if evento in EVENTOS_PASE else f_fin
    return jugada[(jugada["frameId"] >= f_snap) & (jugada["frameId"] <= ultimo)]

"""Modelos Pydantic de las peticiones HTTP."""
from pydantic import BaseModel, Field, model_validator


class SolicitudAnalisis(BaseModel):
    """Qué analizar: una jugada (game_id + play_id), una cobertura o el conjunto global."""
    game_id: int | None = None
    play_id: int | None = None
    cobertura: str | None = Field(default=None, max_length=40)
    pregunta: str | None = Field(default=None, max_length=500)

    @model_validator(mode="after")
    def _ids_completos(self) -> "SolicitudAnalisis":
        if (self.game_id is None) != (self.play_id is None):
            raise ValueError("game_id y play_id deben enviarse juntos")
        return self

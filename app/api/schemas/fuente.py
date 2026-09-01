from datetime import datetime

from pydantic import BaseModel, ConfigDict


class FuenteLeer(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    tipo: str
    referencia_conexion: str
    creado_en: datetime
    
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DatasetLeer(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    fuente_id: int
    nombre: str
    esquema: str
    tabla: str
    creado_en: datetime
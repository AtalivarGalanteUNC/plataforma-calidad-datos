from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class ResultadoLeer(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    check_id: int
    estado: str
    valor_medido: Decimal | None
    mensaje: str | None
    ejecutado_en: datetime
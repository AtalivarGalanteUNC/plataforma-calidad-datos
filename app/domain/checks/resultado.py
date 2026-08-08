from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class ResultadoDeCheck:
    estado: str
    valor_medido: Decimal | None
    mensaje: str | None
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass(frozen=True)
class Cotizacion:
    casa: str
    moneda: str
    compra: Decimal | None
    venta: Decimal | None
    fecha_actualizacion: datetime
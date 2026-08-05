import httpx

from datetime import datetime
from decimal import Decimal

from app.domain.cotizacion import Cotizacion


URL_DOLARES = "https://dolarapi.com/v1/dolares"


class ErrorDolarAPI(Exception):
    """Algo falló al obtener cotizaciones de DolarAPI."""
    pass


def _a_decimal(valor) -> Decimal | None:
    if valor is None:
        return None
    return Decimal(str(valor))


def obtener_cotizaciones() -> list[Cotizacion]:
    try:
        respuesta = httpx.get(URL_DOLARES, timeout=10)
        respuesta.raise_for_status()
        datos_json = respuesta.json()
    except httpx.HTTPError as e:
        raise ErrorDolarAPI(f"No pude obtener las cotizaciones de DolarAPI: {e}") from e

    cotizaciones = []
    for item in datos_json:
        try:
            cotizacion = Cotizacion(
                casa=item["casa"],
                moneda=item["moneda"],
                compra=_a_decimal(item["compra"]),
                venta=_a_decimal(item["venta"]),
                fecha_actualizacion=datetime.fromisoformat(item["fechaActualizacion"]),
            )
        except (KeyError, ValueError) as e:
            raise ErrorDolarAPI(f"DolarAPI devolvió un dato con formato inesperado: {e}") from e
        cotizaciones.append(cotizacion)

    return cotizaciones
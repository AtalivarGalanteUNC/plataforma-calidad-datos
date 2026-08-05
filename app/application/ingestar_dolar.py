from app.infrastructure.dolar_api_client import obtener_cotizaciones
from app.infrastructure.dolar_repositorio import guardar_cotizaciones


def ingestar_dolar() -> int:
    cotizaciones = obtener_cotizaciones()
    guardadas = guardar_cotizaciones(cotizaciones)
    return guardadas
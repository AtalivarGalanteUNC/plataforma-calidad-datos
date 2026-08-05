import os

import psycopg

from app.domain.cotizacion import Cotizacion


SQL_INSERTAR = """
    INSERT INTO dolar (casa, moneda, compra, venta, fecha_actualizacion)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (casa, fecha_actualizacion) DO NOTHING
"""


def guardar_cotizaciones(cotizaciones: list[Cotizacion]) -> int:
    guardadas = 0
    with psycopg.connect(os.environ["ORIGEN_DATABASE_URL"]) as conn:
        with conn.cursor() as cur:
            for c in cotizaciones:
                cur.execute(
                    SQL_INSERTAR,
                    (c.casa, c.moneda, c.compra, c.venta, c.fecha_actualizacion),
                )
                guardadas += cur.rowcount
    return guardadas
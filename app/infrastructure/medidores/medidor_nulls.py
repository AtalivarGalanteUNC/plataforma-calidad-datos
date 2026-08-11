import os
import re
from decimal import Decimal

import psycopg


_IDENTIFICADOR_VALIDO = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")


def _validar_identificador(nombre: str, campo: str) -> str:
    if not _IDENTIFICADOR_VALIDO.match(nombre):
        raise ValueError(f"{campo} inválido: {nombre!r}")
    return nombre


def medir_nulls(
    referencia_conexion: str,
    esquema: str,
    tabla: str,
    columna: str,
) -> tuple[int, Decimal | None]:
    esquema = _validar_identificador(esquema, "esquema")
    tabla = _validar_identificador(tabla, "tabla")
    columna = _validar_identificador(columna, "columna")

    url = os.environ[referencia_conexion]

    sql = (
        f'SELECT count(*), '
        f'count(*) FILTER (WHERE "{columna}" IS NULL) '
        f'FROM "{esquema}"."{tabla}"'
    )

    with psycopg.connect(url) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            total, nulos = cur.fetchone()

    if total == 0:
        return 0, None

    porcentaje = (Decimal(nulos) * Decimal("100") / Decimal(total)).quantize(Decimal("0.01"))
    return total, porcentaje
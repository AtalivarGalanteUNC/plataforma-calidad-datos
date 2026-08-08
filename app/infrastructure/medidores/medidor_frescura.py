import os
import re
from datetime import datetime

import psycopg


_IDENTIFICADOR_VALIDO = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")


def _validar_identificador(nombre: str, campo: str) -> str:
    if not _IDENTIFICADOR_VALIDO.match(nombre):
        raise ValueError(f"{campo} inválido: {nombre!r}")
    return nombre


def medir_frescura(
    referencia_conexion: str,
    esquema: str,
    tabla: str,
    columna: str,
) -> datetime | None:
    esquema = _validar_identificador(esquema, "esquema")
    tabla = _validar_identificador(tabla, "tabla")
    columna = _validar_identificador(columna, "columna")

    url = os.environ[referencia_conexion]

    sql = f'SELECT MAX("{columna}") FROM "{esquema}"."{tabla}"'

    with psycopg.connect(url) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            fila = cur.fetchone()

    return fila[0] if fila else None
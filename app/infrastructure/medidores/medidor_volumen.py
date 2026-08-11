import os
import re

import psycopg


_IDENTIFICADOR_VALIDO = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")


def _validar_identificador(nombre: str, campo: str) -> str:
    if not _IDENTIFICADOR_VALIDO.match(nombre):
        raise ValueError(f"{campo} inválido: {nombre!r}")
    return nombre


def medir_volumen(
    referencia_conexion: str,
    esquema: str,
    tabla: str,
) -> int:
    esquema = _validar_identificador(esquema, "esquema")
    tabla = _validar_identificador(tabla, "tabla")

    url = os.environ[referencia_conexion]

    sql = f'SELECT count(*) FROM "{esquema}"."{tabla}"'

    with psycopg.connect(url) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            fila = cur.fetchone()

    return fila[0]
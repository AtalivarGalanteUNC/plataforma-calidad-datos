from app.application.ejecutar_check import ejecutar_check
from app.infrastructure.db import SessionLocal
from app.infrastructure.repositorio_checks import listar_ids_de_checks_activos


def ejecutar_checks_activos() -> list[tuple[int, str]]:
    with SessionLocal() as session:
        ids = listar_ids_de_checks_activos(session)

    resultados = []
    for check_id in ids:
        try:
            resultado = ejecutar_check(check_id)
            resultados.append((check_id, resultado.estado))
        except Exception as e:
            resultados.append((check_id, f"excepcion: {type(e).__name__}"))

    return resultados
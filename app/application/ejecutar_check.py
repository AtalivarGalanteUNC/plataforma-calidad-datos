from app.domain.checks.estrategia import EstrategiaDeCheck
from app.domain.checks.frescura import ChequeoFrescura
from app.domain.checks.nulls import ChequeoNulls
from app.domain.checks.resultado import ResultadoDeCheck
from app.domain.checks.volumen import ChequeoVolumen
from app.infrastructure.db import SessionLocal
from app.infrastructure.repositorio_checks import obtener_check_por_id
from app.infrastructure.repositorio_resultados import guardar_resultado


class CheckNoEncontrado(Exception):
    pass


class CheckInactivo(Exception):
    pass


class TipoDeCheckDesconocido(Exception):
    pass


def _fabrica_de_estrategias(tipo: str) -> EstrategiaDeCheck:
    if tipo == "frescura":
        return ChequeoFrescura()
    if tipo == "nulls":
        return ChequeoNulls()
    if tipo == "volumen":
        return ChequeoVolumen()
    raise TipoDeCheckDesconocido(f"no conozco el tipo de check: {tipo!r}")


def ejecutar_check(check_id: int) -> ResultadoDeCheck:
    with SessionLocal() as session:
        check = obtener_check_por_id(session, check_id)

        if check is None:
            raise CheckNoEncontrado(f"no existe el check con id {check_id}")

        if not check.activo:
            raise CheckInactivo(f"el check {check_id} está inactivo")

        dataset = check.dataset
        fuente = dataset.fuente
        configuracion = check.configuracion

        try:
            estrategia = _fabrica_de_estrategias(check.tipo)
            medicion = estrategia.medir(fuente, dataset, configuracion)
            resultado = estrategia.ejecutar(medicion, configuracion)
        except Exception as e:
            resultado = ResultadoDeCheck(
                estado="error",
                valor_medido=None,
                mensaje=f"{type(e).__name__}: {e}",
            )

        guardar_resultado(session, check.id, resultado)
        session.commit()

        return resultado
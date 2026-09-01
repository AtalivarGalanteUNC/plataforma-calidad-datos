from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.checks.resultado import ResultadoDeCheck
from app.infrastructure.models import Resultado


def guardar_resultado(
    session: Session,
    check_id: int,
    resultado: ResultadoDeCheck,
) -> int:
    fila = Resultado(
        check_id=check_id,
        estado=resultado.estado,
        valor_medido=resultado.valor_medido,
        mensaje=resultado.mensaje,
    )
    session.add(fila)
    session.flush()
    return fila.id


def listar_resultados(
    session: Session,
    check_id: int | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[Resultado]:
    consulta = select(Resultado)
    if check_id is not None:
        consulta = consulta.where(Resultado.check_id == check_id)
    consulta = consulta.order_by(Resultado.id.desc()).limit(limit).offset(offset)
    return list(session.scalars(consulta))
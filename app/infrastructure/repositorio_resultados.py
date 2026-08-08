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
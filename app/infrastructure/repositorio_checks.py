from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.infrastructure.models import Check
from app.infrastructure.models.dataset import Dataset


def obtener_check_por_id(session: Session, check_id: int) -> Check | None:
    return session.get(
        Check,
        check_id,
        options=[joinedload(Check.dataset).joinedload(Dataset.fuente)],
    )


def listar_ids_de_checks_activos(session: Session) -> list[int]:
    return list(
        session.scalars(
            select(Check.id).where(Check.activo.is_(True)).order_by(Check.id)
        )
    )
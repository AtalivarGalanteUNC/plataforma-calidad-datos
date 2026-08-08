from sqlalchemy.orm import Session, joinedload

from app.infrastructure.models import Check
from app.infrastructure.models.dataset import Dataset


def obtener_check_por_id(session: Session, check_id: int) -> Check | None:
    return session.get(
        Check,
        check_id,
        options=[joinedload(Check.dataset).joinedload(Dataset.fuente)],
    )
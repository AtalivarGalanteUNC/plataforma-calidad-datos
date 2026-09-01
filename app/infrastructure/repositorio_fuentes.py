from sqlalchemy import select
from sqlalchemy.orm import Session

from app.infrastructure.models import Dataset, Fuente


def listar_fuentes(session: Session) -> list[Fuente]:
    return list(session.scalars(select(Fuente).order_by(Fuente.id)))


def listar_datasets(session: Session) -> list[Dataset]:
    return list(session.scalars(select(Dataset).order_by(Dataset.id)))
from datetime import datetime

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Identity, Text, func, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.models.base import Base
from app.infrastructure.models.dataset import Dataset


class Check(Base):
    __tablename__ = "checks"

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    dataset_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("datasets.id"))
    tipo: Mapped[str] = mapped_column(Text)
    nombre: Mapped[str] = mapped_column(Text)
    activo: Mapped[bool] = mapped_column(Boolean, server_default=text("true"))
    configuracion: Mapped[dict] = mapped_column(JSONB)
    creado_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    dataset: Mapped["Dataset"] = relationship()
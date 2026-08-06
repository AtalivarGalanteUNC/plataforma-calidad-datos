from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Identity, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.models.base import Base


class Alerta(Base):
    __tablename__ = "alertas"

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    resultado_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("resultados.id"))
    canal: Mapped[str] = mapped_column(Text)
    estado: Mapped[str] = mapped_column(Text)
    enviada_en: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    creado_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
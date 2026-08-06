from datetime import datetime
from decimal import Decimal

from sqlalchemy import BigInteger, DateTime, ForeignKey, Identity, Numeric, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.models.base import Base


class Resultado(Base):
    __tablename__ = "resultados"

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    check_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("checks.id"))
    estado: Mapped[str] = mapped_column(Text)
    valor_medido: Mapped[Decimal | None] = mapped_column(Numeric(12, 2))
    mensaje: Mapped[str | None] = mapped_column(Text)
    ejecutado_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
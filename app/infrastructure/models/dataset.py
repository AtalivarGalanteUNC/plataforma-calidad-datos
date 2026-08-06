from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Identity, Text, func, text
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.models.base import Base


class Dataset(Base):
    __tablename__ = "datasets"

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    fuente_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("fuentes.id"))
    nombre: Mapped[str] = mapped_column(Text)
    esquema: Mapped[str] = mapped_column(Text, server_default=text("'public'"))
    tabla: Mapped[str] = mapped_column(Text)
    creado_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
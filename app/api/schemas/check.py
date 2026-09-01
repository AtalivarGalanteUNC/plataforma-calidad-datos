from datetime import datetime

from pydantic import BaseModel, ConfigDict, ValidationError, model_validator

from app.api.schemas.config import SCHEMAS_CONFIG


class CheckCrear(BaseModel):
    dataset_id: int
    tipo: str
    nombre: str
    configuracion: dict

    @model_validator(mode="after")
    def validar_config_segun_tipo(self):
        schema = SCHEMAS_CONFIG.get(self.tipo)
        if schema is None:
            raise ValueError(
                f"tipo de check desconocido: {self.tipo!r}. "
                f"tipos válidos: {sorted(SCHEMAS_CONFIG)}"
            )
        try:
            config_validada = schema(**self.configuracion)
        except ValidationError as e:
            raise ValueError(
                f"configuración inválida para tipo {self.tipo!r}: {e}"
            )
        self.configuracion = config_validada.model_dump()
        return self


class CheckLeer(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    dataset_id: int
    tipo: str
    nombre: str
    activo: bool
    configuracion: dict
    creado_en: datetime
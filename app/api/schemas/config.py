from pydantic import BaseModel, ConfigDict, Field, model_validator


class ConfigFrescura(BaseModel):
    model_config = ConfigDict(extra="forbid")

    columna: str
    umbral_horas: float = Field(gt=0)


class ConfigNulls(BaseModel):
    model_config = ConfigDict(extra="forbid")

    columna: str
    umbral_pct: float = Field(ge=0, le=100)


class ConfigVolumen(BaseModel):
    model_config = ConfigDict(extra="forbid")

    min_filas: int = Field(ge=0)
    max_filas: int = Field(ge=0)

    @model_validator(mode="after")
    def validar_rango(self):
        if self.min_filas > self.max_filas:
            raise ValueError("min_filas no puede ser mayor que max_filas")
        return self


SCHEMAS_CONFIG = {
    "frescura": ConfigFrescura,
    "nulls": ConfigNulls,
    "volumen": ConfigVolumen,
}
from decimal import Decimal

from app.domain.checks.estrategia import EstrategiaDeCheck
from app.domain.checks.resultado import ResultadoDeCheck
from app.infrastructure.medidores.medidor_nulls import medir_nulls
from app.infrastructure.models import Dataset, Fuente


class ChequeoNulls(EstrategiaDeCheck):
    def medir(
        self,
        fuente: Fuente,
        dataset: Dataset,
        configuracion: dict,
    ) -> tuple[int, Decimal | None]:
        return medir_nulls(
            referencia_conexion=fuente.referencia_conexion,
            esquema=dataset.esquema,
            tabla=dataset.tabla,
            columna=configuracion["columna"],
        )

    def ejecutar(
        self,
        medicion: tuple[int, Decimal | None],
        configuracion: dict,
    ) -> ResultadoDeCheck:
        umbral_pct = Decimal(str(configuracion["umbral_pct"]))
        total, porcentaje = medicion

        if total == 0:
            return ResultadoDeCheck(
                estado="fallo",
                valor_medido=None,
                mensaje="la tabla está vacía, no hay dato para medir nulls",
            )

        if porcentaje <= umbral_pct:
            return ResultadoDeCheck(
                estado="paso",
                valor_medido=porcentaje,
                mensaje=None,
            )

        return ResultadoDeCheck(
            estado="fallo",
            valor_medido=porcentaje,
            mensaje=(
                f"el {porcentaje}% de nulls supera "
                f"el umbral de {umbral_pct}%"
            ),
        )
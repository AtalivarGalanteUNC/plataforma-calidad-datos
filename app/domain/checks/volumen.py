from decimal import Decimal

from app.domain.checks.estrategia import EstrategiaDeCheck
from app.domain.checks.resultado import ResultadoDeCheck
from app.infrastructure.medidores.medidor_volumen import medir_volumen
from app.infrastructure.models import Dataset, Fuente


class ChequeoVolumen(EstrategiaDeCheck):
    def medir(
        self,
        fuente: Fuente,
        dataset: Dataset,
        configuracion: dict,
    ) -> int:
        return medir_volumen(
            referencia_conexion=fuente.referencia_conexion,
            esquema=dataset.esquema,
            tabla=dataset.tabla,
        )

    def ejecutar(
        self,
        medicion: int,
        configuracion: dict,
    ) -> ResultadoDeCheck:
        min_filas = Decimal(str(configuracion["min_filas"]))
        max_filas = Decimal(str(configuracion["max_filas"]))
        filas_medidas = Decimal(medicion)

        if filas_medidas < min_filas:
            return ResultadoDeCheck(
                estado="fallo",
                valor_medido=filas_medidas,
                mensaje=(
                    f"hay {medicion} filas, menos que el mínimo "
                    f"esperado de {int(min_filas)}"
                ),
            )

        if filas_medidas > max_filas:
            return ResultadoDeCheck(
                estado="fallo",
                valor_medido=filas_medidas,
                mensaje=(
                    f"hay {medicion} filas, más que el máximo "
                    f"esperado de {int(max_filas)}"
                ),
            )

        return ResultadoDeCheck(
            estado="paso",
            valor_medido=filas_medidas,
            mensaje=None,
        )
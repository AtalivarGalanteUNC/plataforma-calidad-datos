from datetime import datetime, timezone
from decimal import Decimal

from app.domain.checks.estrategia import EstrategiaDeCheck
from app.domain.checks.resultado import ResultadoDeCheck


class ChequeoFrescura(EstrategiaDeCheck):
    def ejecutar(
        self,
        medicion: datetime | None,
        configuracion: dict,
    ) -> ResultadoDeCheck:
        umbral_horas = Decimal(str(configuracion["umbral_horas"]))

        if medicion is None:
            return ResultadoDeCheck(
                estado="fallo",
                valor_medido=None,
                mensaje="la tabla está vacía, no hay dato para medir la frescura",
            )

        ahora = datetime.now(timezone.utc)
        antiguedad_segundos = Decimal(str((ahora - medicion).total_seconds()))
        antiguedad_horas = (antiguedad_segundos / Decimal("3600")).quantize(Decimal("0.01"))

        if antiguedad_horas <= umbral_horas:
            return ResultadoDeCheck(
                estado="paso",
                valor_medido=antiguedad_horas,
                mensaje=None,
            )

        return ResultadoDeCheck(
            estado="fallo",
            valor_medido=antiguedad_horas,
            mensaje=(
                f"la antigüedad de {antiguedad_horas} horas "
                f"supera el umbral de {umbral_horas} horas"
            ),
        )
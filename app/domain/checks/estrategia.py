from abc import ABC, abstractmethod
from typing import Any

from app.domain.checks.resultado import ResultadoDeCheck
from app.infrastructure.models import Dataset, Fuente


class EstrategiaDeCheck(ABC):
    @abstractmethod
    def medir(
        self,
        fuente: Fuente,
        dataset: Dataset,
        configuracion: dict,
    ) -> Any:
        ...

    @abstractmethod
    def ejecutar(self, medicion: Any, configuracion: dict) -> ResultadoDeCheck:
        ...
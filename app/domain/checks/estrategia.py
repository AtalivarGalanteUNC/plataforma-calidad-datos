from abc import ABC, abstractmethod
from typing import Any

from app.domain.checks.resultado import ResultadoDeCheck


class EstrategiaDeCheck(ABC):
    @abstractmethod
    def ejecutar(self, medicion: Any, configuracion: dict) -> ResultadoDeCheck:
        ...
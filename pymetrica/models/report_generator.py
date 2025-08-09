from abc import ABC, abstractmethod
from typing import TypeVar

from .metric import Metric, Results

T = TypeVar("T", bound=Results)


class ReportGenerator(ABC):
    @abstractmethod
    def generate_report(self, metrics: list[Metric[T]]) -> str:
        raise NotImplementedError(
            "Subclasses of ReportGenerator must implement this method.",
        )

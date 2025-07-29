from abc import ABC, abstractmethod

from .metric import Metric, Results
from typing import TypeVar


T = TypeVar("T", bound=Results)


class ReportGenerator(ABC):
    @abstractmethod
    def generate_report(self, metrics: list[Metric[T]]) -> None:
        raise NotImplementedError(
            "Subclasses of ReportGenerator must implement this method."
        )

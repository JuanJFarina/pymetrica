from abc import ABC, abstractmethod

from .metric import Metric


class ReportGenerator(ABC):
    @abstractmethod
    def generate_report(self, metrics: list[Metric]) -> None:
        raise NotImplementedError("Subclasses of ReportGenerator must implement this method.")

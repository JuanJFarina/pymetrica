from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from .codebase import Codebase
from .metric import Metric, Results

T = TypeVar("T", bound=Results)


class MetricCalculator(ABC, Generic[T]):
    @abstractmethod
    def calculate_metric(self, codebase: Codebase) -> Metric[T]:
        raise NotImplementedError(
            "Subclasses of MetricCalculator must implement this method.",
        )

from abc import ABC, abstractmethod

from pymetrica.models import Codebase, Metric, Results
from typing import Generic, TypeVar

T = TypeVar("T", bound=Results)


class MetricCalculator(ABC, Generic[T]):
    @abstractmethod
    def calculate_metric(self, codebase: Codebase) -> Metric[T]:
        raise NotImplementedError(
            "Subclasses of MetricCalculator must implement this method."
        )

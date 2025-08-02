from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import Generic
from typing import TypeVar

from pymetrica.models import Codebase
from pymetrica.models import Metric
from pymetrica.models import Results

T = TypeVar('T', bound=Results)


class MetricCalculator(ABC, Generic[T]):
    @abstractmethod
    def calculate_metric(self, codebase: Codebase) -> Metric[T]:
        raise NotImplementedError(
            'Subclasses of MetricCalculator must implement this method.',
        )

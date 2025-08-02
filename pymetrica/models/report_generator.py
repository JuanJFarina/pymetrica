from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import TypeVar

from .metric import Metric
from .metric import Results


T = TypeVar('T', bound=Results)


class ReportGenerator(ABC):
    @abstractmethod
    def generate_report(self, metrics: list[Metric[T]]) -> None:
        raise NotImplementedError(
            'Subclasses of ReportGenerator must implement this method.',
        )

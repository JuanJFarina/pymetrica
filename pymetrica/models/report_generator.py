import sys
from abc import ABC, abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any, TypeVar

import click
from pydantic import BaseModel

from .metric import Metric, Results

T = TypeVar("T", bound=Results)


class Report(BaseModel):
    content: str
    exit_status: int = 0

    def echo_and_exit(self) -> None:
        click.echo(self.content)
        if self.exit_status:
            sys.exit(self.exit_status)


@dataclass
class ReportGenerator(ABC):
    metrics: Sequence[Metric[Any]]

    @property
    @abstractmethod
    def short_report(self) -> Report:
        raise NotImplementedError(
            "Subclasses of ReportGenerator must implement this method.",
        )

    @property
    @abstractmethod
    def long_report(self) -> Report:
        raise NotImplementedError(
            "Subclasses of ReportGenerator must implement this method.",
        )

    @property
    def exit_status(self) -> int:
        return sum(
            metric.exit_code for metric in self.metrics if metric.exceeds_threshold
        )

    @property
    def fail_messages(self) -> str:
        return "\n".join(
            metric.fail_message for metric in self.metrics if metric.exceeds_threshold
        )

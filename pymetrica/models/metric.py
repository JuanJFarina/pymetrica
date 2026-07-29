from abc import ABC, abstractmethod
from collections.abc import Mapping
from typing import Any, Generic, Protocol, TypeVar

from pydantic import BaseModel, ConfigDict

_NIE_MSG = "Subclasses of Results must implement this method."


class Results(BaseModel, ABC):
    @property
    @abstractmethod
    def json_(self) -> str:
        raise NotImplementedError(_NIE_MSG)

    @property
    @abstractmethod
    def dict_(self) -> dict[str, Any]:
        raise NotImplementedError(_NIE_MSG)


T = TypeVar("T", bound=Results)


class ReportableMetric(Protocol):
    @property
    def name(self) -> str: ...

    @property
    def description(self) -> str: ...

    @property
    def exit_code(self) -> int: ...

    @property
    def results_dict(self) -> Mapping[str, object]: ...

    @property
    def summary(self) -> str: ...

    @property
    def fail_message(self) -> str: ...

    def exceeds_threshold(self, audit: bool = False) -> bool: ...


class Metric(ABC, BaseModel, Generic[T]):
    name: str
    description: str
    results: T
    exit_code: int

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @property
    def results_dict(self) -> dict[str, Any]:
        return self.results.dict_

    @property
    @abstractmethod
    def summary(self) -> str:
        raise NotImplementedError(_NIE_MSG)

    @property
    @abstractmethod
    def fail_message(self) -> str:
        raise NotImplementedError(_NIE_MSG)

    @abstractmethod
    def exceeds_threshold(self, audit: bool = False) -> bool:
        raise NotImplementedError(_NIE_MSG)

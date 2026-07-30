from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

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

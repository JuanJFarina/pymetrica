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

    @property
    @abstractmethod
    def summary(self) -> str:
        raise NotImplementedError(_NIE_MSG)

    @property
    @abstractmethod
    def fail_message(self) -> str:
        raise NotImplementedError(_NIE_MSG)

    @property
    @abstractmethod
    def exceeds_threshold(self) -> bool:
        raise NotImplementedError(_NIE_MSG)


T_co = TypeVar("T_co", bound=Results, covariant=True)


class Metric(BaseModel, Generic[T_co]):
    name: str
    description: str
    results: T_co
    exit_code: int

    model_config = ConfigDict(arbitrary_types_allowed=True)

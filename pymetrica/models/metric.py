from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict

_NIE_MSG = "Subclasses of Results must implement this method."


class Results(BaseModel, ABC):
    @abstractmethod
    def get_json(self) -> str:
        raise NotImplementedError(_NIE_MSG)

    @abstractmethod
    def get_dict(self) -> dict[str, Any]:
        raise NotImplementedError(_NIE_MSG)

    @abstractmethod
    def get_summary(self) -> str:
        raise NotImplementedError(_NIE_MSG)

    @abstractmethod
    def get_fail_message(self, fail_threshold: int) -> str:
        raise NotImplementedError(_NIE_MSG)


T_co = TypeVar("T_co", bound=Results, covariant=True)


class Metric(BaseModel, Generic[T_co]):
    name: str
    description: str
    results: T_co

    model_config = ConfigDict(arbitrary_types_allowed=True)

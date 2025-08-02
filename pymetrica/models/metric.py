from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Generic
from typing import TypeVar

from pydantic import BaseModel


class Results(BaseModel, ABC):
    @abstractmethod
    def get_json(self) -> str:
        raise NotImplementedError(
            'Subclasses of Results must implement this method.',
        )

    @abstractmethod
    def get_dict(self) -> dict[str, Any]:
        raise NotImplementedError(
            'Subclasses of Results must implement this method.',
        )

    @abstractmethod
    def get_summary(self) -> str:
        raise NotImplementedError(
            'Subclasses of Results must implement this method.',
        )


T = TypeVar('T', bound=Results)


class Metric(BaseModel, Generic[T]):
    name: str
    description: str
    results: T

    class Config:
        arbitrary_types_allowed = True

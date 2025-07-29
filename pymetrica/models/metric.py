from pydantic import BaseModel
from typing import Any, TypeVar, Generic
from abc import ABC, abstractmethod


class Results(BaseModel, ABC):
    @abstractmethod
    def get_json(self) -> str:
        raise NotImplementedError("Subclasses of Results must implement this method.")

    @abstractmethod
    def get_dict(self) -> dict[str, Any]:
        raise NotImplementedError("Subclasses of Results must implement this method.")

    @abstractmethod
    def get_summary(self) -> str:
        raise NotImplementedError("Subclasses of Results must implement this method.")


T = TypeVar("T", bound=Results)


class Metric(BaseModel, Generic[T]):
    name: str
    description: str
    results: T

    class Config:
        arbitrary_types_allowed = True

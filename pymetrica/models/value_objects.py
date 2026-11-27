from typing import Annotated

from pydantic import Field, StringConstraints

StrPath = Annotated[str, StringConstraints(min_length=1)]
StrRatio = Annotated[
    str,
    StringConstraints(pattern=r"^\d+(?:\.\d+)?:\d+(?:\.\d+)?$"),
]
PositiveInt = Annotated[int, Field(ge=0)]

__all__ = ["PositiveInt", "StrPath", "StrRatio"]

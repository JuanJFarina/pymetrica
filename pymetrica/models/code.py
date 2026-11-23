from pydantic import BaseModel

from .value_objects import NonNegativeInt, StrPath


class Code(BaseModel):
    filepath: StrPath
    filename: str
    lloc_number: NonNegativeInt
    comments_number: NonNegativeInt
    code_lines: list[str]
    code: str

    aloc_number: int | None = None
    cc_number: int | None = None
    hv_number: float | None = None
    all_primitives: int | None = None
    targeted_primitives: int | None = None

    @property
    def maintainability_cost(self) -> float:
        hv = self.hv_number or 0
        cc = self.cc_number or 0
        complexity = (hv * ((cc) * 100 or 1)) / 20
        return complexity + self.lloc_number * 0.001

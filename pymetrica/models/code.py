from pydantic import BaseModel


class Code(BaseModel):
    filepath: str
    filename: str
    lloc_number: int
    comments_number: int
    code_lines: list[str]
    code: str

    aloc_number: int | None = None
    cc_number: int | None = None
    hv_number: float | None = None
    all_primitives: int | None = None
    targeted_primitives: int | None = None

    @property
    def maintainability_cost(self) -> float:
        hv_density = (self.hv_number or 0) / (self.lloc_number or 1)
        cc_density = (self.cc_number or 0) / (self.lloc_number or 1)
        average_lloc_mc = (hv_density * ((cc_density) * 100 or 1)) / 20
        return average_lloc_mc + self.lloc_number * 0.001

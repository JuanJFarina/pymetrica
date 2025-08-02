from __future__ import annotations

from pydantic import BaseModel


class Code(BaseModel):
    filepath: str
    filename: str
    lloc_number: int
    comments_number: int
    code_lines: list[str]
    code: str

import sys
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, model_validator

from .logging import log

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib


def find_pyproject() -> Path | None:
    path = Path.cwd() / "pyproject.toml"
    return path if path.exists() else None


class Configuration(BaseModel):
    aloc_fail_threshold: int = 30
    cc_fail_threshold: int = 7
    hv_fail_threshold: int = 30
    mc_fail_threshold: int = 25
    po_all_fail_threshold: int = 10
    po_targeted_fail_threshold: int = 2
    exclude: list[str] = []
    top_findings: int = 5

    @model_validator(mode="before")
    @classmethod
    def read_from_pyproject_toml(cls, data: Any) -> Any:
        path = Path.cwd() / "pyproject.toml"
        if not path.exists():
            log.warning("Pyproject.toml not found")
            return data
        with open(path, mode="rb") as config_path:
            content = tomllib.load(config_path)
        try:
            sections_values = content["tool"]["pymetrica"]
        except KeyError:
            log.warning(
                "Pymetrica configurations not found in pyproject.toml, use [tool.pymetrica]",
            )
            return data
        log.info(
            f"Configuration values taken from pyproject.toml values: {sections_values}",
        )
        return sections_values

    @property
    def find_top_flaws(self) -> bool:
        return self.top_findings > 0

    model_config = ConfigDict(extra="ignore")


Config = Configuration()  # pylint: disable=invalid-name

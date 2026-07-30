import sys
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from .logging import log

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib


def find_pyproject(directory: str) -> Path | None:
    target = Path(directory).resolve()
    for parent in (target, *target.parents):
        path = parent / "pyproject.toml"
        if path.is_file():
            with path.open(mode="rb") as config_path:
                content = tomllib.load(config_path)
            if content.get("tool", {}).get("pymetrica") is not None:
                return path
        if (parent / ".git").exists():
            return None
    return None


class Configuration(BaseModel):
    aloc_fail_threshold: int = 30
    cc_fail_threshold: int = 7
    hv_fail_threshold: int = 30
    mc_fail_threshold: int = 25
    po_all_fail_threshold: int = 10
    po_targeted_fail_threshold: int = 2
    exclude: list[str] = Field(default_factory=list)
    top_findings: int = 5

    @property
    def find_top_flaws(self) -> bool:
        return self.top_findings > 0

    def update_config(self, **kwargs: Any) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)

    model_config = ConfigDict(extra="ignore")


Config = Configuration()  # pylint: disable=invalid-name


def update_config_from_pyproject(directory: str) -> None:
    path = find_pyproject(directory)
    if path is None:
        log.warning("Pymetrica configuration not found")
        return
    with open(path, mode="rb") as config_path:
        content = tomllib.load(config_path)
    try:
        sections_values = content["tool"]["pymetrica"]
    except KeyError:
        log.warning(
            "Pymetrica configurations not found in pyproject.toml, use [tool.pymetrica]",
        )
        return
    log.info(
        f"Configuration values taken from pyproject.toml values: {sections_values}",
    )
    Config.update_config(**sections_values)

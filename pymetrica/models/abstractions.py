from __future__ import annotations

from pydantic import BaseModel


class Abstraction(BaseModel):
    hash: str
    name: str
    depth_level: int
    parent_container_name: str | None


class Dependency(BaseModel):
    target: str
    weight: int


class Component(Abstraction):
    concrete_modules: list[str]
    dependencies: list[Dependency]


class Container(Abstraction):
    concrete_packages: list[str]
    childs: list[Component | Container]

from pydantic import BaseModel


class Abstraction(BaseModel):
    hash: str
    name: str
    depth_level: int
    parent_container_name: str


class Component(Abstraction):
    concrete_modules: list[str]
    dependencies: list[str]


class Container(Abstraction):
    concrete_packages: list[str]
    childs: list[Abstraction]

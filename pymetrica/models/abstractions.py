from pydantic import BaseModel

from .code import Code

Folder = str


class Abstraction(BaseModel):
    hash: str
    name: str
    dependencies: list[str]


class Component(Abstraction):
    """Equals one or more python modules (.py files)"""
    depth_level: int
    parent_container: Abstraction
    sources: list[Code]


class Container(Abstraction):
    """Equals one or more python subpackages (folders)"""
    depth_level: int
    parent_container: Abstraction | None
    child_components: list[Component]
    sources: list[str]


class HigherOrderContainer(Abstraction):
    """Equals one or more python packages or subpackages (folders) that contain other subpackages"""
    depth_level: int
    child_containers: list[Container]
    sources: list[str]

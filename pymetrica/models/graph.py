from pydantic import BaseModel


class Node(BaseModel):
    name: str
    dependencies: list[str]


class Edge(BaseModel):
    source: str
    target: str
    weight: int


class Graph(BaseModel):
    nodes: list[Node]
    edges: list[Edge]

from abc import ABC

class Metric(ABC):
    name: str
    description: str = ""
    value: float

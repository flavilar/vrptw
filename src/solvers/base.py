from abc import ABC, abstractmethod
from typing import List


class Solver(ABC):
    """Abstract base for VRPTW solvers."""

    def __init__(self, instance):
        self.instance = instance

    @abstractmethod
    def solve(self) -> List:
        """Return a list of Route objects."""
        ...

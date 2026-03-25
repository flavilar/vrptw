from abc import ABC, abstractmethod


class LocalSearch(ABC):
    """Abstract base for route-level local search operators."""

    @abstractmethod
    def optimize(self, route):
        """Modify route in place. Return None."""
        ...

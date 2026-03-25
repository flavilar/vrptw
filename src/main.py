import sys
import os

# Add vrptw root to path so 'src' is importable as a package
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from src.parser import read_solomon_instance
from src.solvers import GreedySolver
from src.local_search.two_opt import TwoOptLocalSearch


def main():
    print("VRPTW environment ready")
    print("NumPy version:", np.__version__)

    instance = read_solomon_instance("data/benchmarks/solomon-100/r102.txt")
    print(instance)

    # Swap in any Solver implementation here
    solver = GreedySolver(instance)
    routes = solver.solve()
    print(routes)

    # Swap in any LocalSearch implementation here
    local_search = TwoOptLocalSearch()
    for route in routes:
        local_search.optimize(route)
    print(routes)


if __name__ == "__main__":
    main()

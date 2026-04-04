import sys
from pathlib import Path

# Get repo root (one level above src/)
root = Path(__file__).resolve().parent.parent

# Add vrptw root to path so 'src' is importable as a package
sys.path.insert(0, str(root))

import numpy as np
from src.parser import read_solomon_instance
from src.solvers import GreedySolver
from src.local_search import TwoOptLocalSearch



def main():
    print("VRPTW environment ready")
    print("NumPy version:", np.__version__)

    # Build your path relative to repo root
    data_path = root / "data" / "benchmarks" / "solomon-100" / "r102.txt"

    instance = read_solomon_instance(data_path)
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

from .base import Solver
from src.route import Route
from src.utils import calculate_euclidean_matrix


class GreedySolver(Solver):
    """Nearest-neighbor heuristic with capacity + time window feasibility."""

    def __init__(self, instance):
        super().__init__(instance)

    def solve(self):
        dist_matrix = calculate_euclidean_matrix(self.instance.nodes)
        unvisited = self.instance.nodes[1:].copy()
        routes = []

        while unvisited:
            current_route = Route(self.instance, dist_matrix)
            while True:
                best_node = None
                min_dist = float('inf')
                current_node = current_route.last_node

                for candidate in unvisited:
                    dist = dist_matrix[current_node][candidate]
                    if dist < min_dist and current_route.is_feasible(candidate):
                        min_dist = dist
                        best_node = candidate

                if best_node:
                    current_route.add_node(best_node)
                    unvisited.remove(best_node)
                else:
                    break

            current_route.close_route()
            routes.append(current_route)

        return routes

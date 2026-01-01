import numpy as np
from src.utils import calculate_euclidean_matrix


class Route:
    def __init__(self, instance, dist_matrix):
        self.capacity = instance.capacity
        self.depot = instance.nodes[0]
        self.dist_matrix = dist_matrix

        # Sequence of Node Objects
        self.sequence = [self.depot]
        self.load = 0.0
        self.time = 0.0
        self.cost = 0.0
        self.is_closed = False

    @property
    def last_node(self):
        return self.sequence[-1]

    def is_feasible(self, node):
        if self.is_closed: return False

        if self.load + node.demand > self.capacity:
            return False

        prev_node = self.last_node

        dist = self.dist_matrix[prev_node][node]
        departure_time = max(self.time, prev_node.ready_time) + prev_node.service_time
        arrival_time = departure_time + dist

        if arrival_time > node.due_date:
            return False

        return True

    def add_node(self, node):
        prev_node = self.last_node

        dist = self.dist_matrix[prev_node][node]

        self.load += node.demand

        departure_from_prev = max(self.time, prev_node.ready_time) + prev_node.service_time
        arrival_at_new = departure_from_prev + dist

        self.time = max(arrival_at_new, node.ready_time)
        self.cost += dist
        self.sequence.append(node)

    def close_route(self):
        if self.is_closed: return
        # Try to return to depot
        if self.is_feasible(self.depot):
            self.add_node(self.depot)
        else:
            print("Unable to reach depot when trying to close route!")
            self.add_node(self.depot)  # Force close
        self.is_closed = True

    def __repr__(self):
        path_ids = [n.id for n in self.sequence]
        return f"Route(Load={self.load}, Cost={self.cost:.2f}, Path={path_ids})"


class GreedySolver:
    def __init__(self, instance):
        self.instance = instance
        self.dist_matrix = calculate_euclidean_matrix(instance.nodes)
        self.routes = []

    def solve(self):
        unvisited = self.instance.nodes[1:].copy()

        while unvisited:
            current_route = Route(self.instance, self.dist_matrix)
            while True:
                best_node = None
                min_dist = float('inf')
                current_node = current_route.last_node

                for candidate in unvisited:
                    dist = self.dist_matrix[current_node][candidate]

                    if dist < min_dist:
                        if current_route.is_feasible(candidate):
                            min_dist = dist
                            best_node = candidate

                if best_node:
                    current_route.add_node(best_node)
                    unvisited.remove(best_node)
                else:
                    break

            current_route.close_route()
            self.routes.append(current_route)
        return self.routes


class LocalSearch:
    """
    Implements 2-Opt.
    """

    def __init__(self):
        self.dist_matrix = None

    def optimize_route(self, route):
        """
        Applies 2-Opt to a single Route object to reduce its distance.
        This modifies the 'route.sequence' in place.
        """
        self.dist_matrix = route.dist_matrix
        improved = True
        while improved:
            improved = False
            n = len(route.sequence)

            for i in range(1, n - 2):
                for j in range(i + 1, n - 1):
                    # Current edges: (i-1 -> i) and (j -> j+1)
                    # Candidate edges: (i-1 -> j) and (i -> j+1)
                    # Reverses the segment between i and j

                    if self._calculate_2opt_gain(route.sequence, i, j) < 0:
                        # If gain is negative, it means distance decreases
                        self._apply_2opt_swap(route.sequence, i, j)
                        route.cost = self._recalculate_cost(route.sequence)
                        improved = True

            # TODO: In a full VRPTW implementation, is_feasible() must be checked here.

    def _calculate_2opt_gain(self, sequence, i, j):
        """
        Calculates the change in distance if we swap.
        """
        a = sequence[i - 1]
        b = sequence[i]
        c = sequence[j]
        d = sequence[j + 1]

        d_current = self.dist_matrix[a][b] + self.dist_matrix[c][d]
        d_new = self.dist_matrix[a][c] + self.dist_matrix[b][d]

        return d_new - d_current

    def _apply_2opt_swap(self, sequence, i, j):
        """
        Reverses the sub-segment of the list.
        """
        sequence[i:j + 1] = reversed(sequence[i:j + 1])

    def _recalculate_cost(self, sequence):
        cost = 0.0
        for k in range(len(sequence) - 1):
            cost += self.dist_matrix[sequence[k]][sequence[k + 1]]
        return cost
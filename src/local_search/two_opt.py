from .base import LocalSearch


class TwoOptLocalSearch(LocalSearch):
    """
    2-opt local search operator.
    Swaps edges within a single route to reduce distance.

    TODO: feasibility checks (time windows, capacity) not yet implemented.
          Swaps that break constraints are currently accepted.
    """

    def optimize(self, route):
        improved = True
        while improved:
            improved = False
            n = len(route.sequence)

            for i in range(1, n - 2):
                for j in range(i + 1, n - 1):
                    if self._gain(route.sequence, i, j, route.dist_matrix) < 0:
                        self._swap(route.sequence, i, j)
                        route.recalculate_cost()
                        improved = True

    def _gain(self, sequence, i, j, dist_matrix):
        a, b = sequence[i - 1], sequence[i]
        c, d = sequence[j], sequence[j + 1]
        return (dist_matrix[a][c] + dist_matrix[b][d]) - \
               (dist_matrix[a][b] + dist_matrix[c][d])

    def _swap(self, sequence, i, j):
        sequence[i:j + 1] = reversed(sequence[i:j + 1])

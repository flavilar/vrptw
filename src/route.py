import numpy as np


class Node:
    """Solomon benchmark customer node."""
    def __init__(self, id, x, y, demand, ready_time, due_date, service_time):
        self.id = id
        self.x = x
        self.y = y
        self.demand = demand
        self.ready_time = ready_time
        self.due_date = due_date
        self.service_time = service_time

    def __index__(self):
        return self.id

    def __repr__(self):
        return f"Node({self.id}, ({self.x},{self.y}), d={self.demand}, tw=[{self.ready_time},{self.due_date}])"


class Route:
    def __init__(self, instance, dist_matrix):
        self.capacity = instance.capacity
        self.depot = instance.nodes[0]
        self.dist_matrix = dist_matrix

        self.sequence = [self.depot]
        self.load = 0.0
        self.time = 0.0
        self.cost = 0.0
        self.is_closed = False

    @property
    def last_node(self):
        return self.sequence[-1]

    def is_feasible(self, node):
        if self.is_closed:
            return False
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
        if self.is_closed:
            return
        if self.is_feasible(self.depot):
            self.add_node(self.depot)
        else:
            print("Unable to reach depot when trying to close route!")
            self.add_node(self.depot)
        self.is_closed = True

    def recalculate_cost(self):
        self.cost = sum(
            self.dist_matrix[self.sequence[k]][self.sequence[k + 1]]
            for k in range(len(self.sequence) - 1)
        )

    def __repr__(self):
        path_ids = [n.id for n in self.sequence]
        return f"Route(Load={self.load}, Cost={self.cost:.2f}, Path={path_ids})"

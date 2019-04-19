# import numpy as np
import copy

squared_euclid_error = 100.0     # squared  cutoff distance for critical points to be considered "equal"?


class CriticalPoint:
    def __init__(self, x, y, crit_type, birth_time):
        self.x = x                                  # x coordinate, float
        self.y = y                                  # y coordinate, float
        self.crit_type = crit_type                  # critical point type, either 'max' or 'min', char[]
        self.birth_time = birth_time
        self.death_time = None

    def __eq__(self, other):
        if self.crit_type != other.crit_type:
            return False
        if (self.x - other.x) ** 2 + (self.y - other.y) ** 2 > squared_euclid_error:
            return False

        return True


class Node:
    def __init__(self, critical_point):
        self.critical_point = critical_point       # CriticalPoint of node
        self.left = None                           # Left node reference
        self.right = None                          # Right node reference

    def append_right(self, node):
        self.right = node

    def append_left(self, node):
        self.left = node

    def __eq__(self, other):
        if self.critical_point != other.critical_point:
            return False

        return True


class Graph:
    # Initialization requires at least one critical point
    def __init__(self, time):
        self.nodes = []
        self.time = time

    # Critical points MUST be added by traversing the curve of the boundary
    def add_node(self, critical_point):
        node = Node(critical_point)
        if node not in self.nodes:
            self.nodes.append(copy.deepcopy(node))
            self.nodes[len(self.nodes) - 1].append_left(self.nodes[len(self.nodes) - 2])
            self.nodes[len(self.nodes) - 2].append_right(self.nodes[len(self.nodes) - 1])

    # Delete node and update references
    def delete_node(self, node):
        if len(self.nodes) == 0:
            return
        for i in range(0, len(self.nodes)):
            if self.nodes[i] == node:
                if i == 0:
                    self.nodes[i + 1].left = None
                elif i == len(self.nodes) - 1:
                    self.nodes[i - 1].right = None
                else:
                    self.nodes[i + 1].left = self.nodes[i - 1]
                    self.nodes[i - 1].right = self.nodes[i + 1]

                self.nodes.remove(node)
                return

    # Reduce noisy critical points. Keep older living critical points. Call after adding all nodes to graph
    def smooth_bumps(self):
        changed_flag = True
        while changed_flag:
            changed_flag = False
            for i in range(0, len(self.nodes) - 1):
                if self.nodes[i].critical_point == self.nodes[i + 1].critical_point:
                    changed_flag = True
                    if self.nodes[i].critical_point.birth_time < self.nodes[i + 1].critical_point.birth_time:
                        self.delete_node(self.nodes[i + 1])
                    else:
                        self.delete_node(self.nodes[i])
                    break

    # This compares a previous time-step graph and returns critical points that were born and those that died
    def compare_with_previous_graph(self, previous_graph):
        critical_points_born = []
        critical_points_died = []

        # this part needs to be discussed more and finished maybe together? Current version is naive. If a previous
        # graph does not contain the critical point, then it has been born. If the new graph does not contain a
        # previous critical point, it has died
        for node in self.nodes:
            if node not in previous_graph.nodes:
                critical_points_born.append(copy.deepcopy(node.critical_point))

        # Update born times of "same" nodes
        for node in self.nodes:
            if node in previous_graph.nodes:
                ndx = previous_graph.nodes.index(node)
                node.critical_point.birth_time = previous_graph.nodes[ndx].critical_point.birth_time

        for node in previous_graph.nodes:
            if node not in self.nodes:
                node.critical_point.death_time = self.time
                critical_points_died.append(copy.deepcopy(node.critical_point))

        return [critical_points_born, critical_points_died]


class PersistenceDiagram:
    def __init__(self, graphs, end_time):
        self.graphs = graphs                      # Python list of Graph objects
        self.end_time = end_time                  # int or float defining end time of graph generation
        self.diagram = []        # Python list of [,] birth/death pair

    def generate_diagram(self):
        points = []
        for i in range(1, len(self.graphs)):
            for critical_point in self.graphs[i].compare_with_previous_graph(self.graphs[i - 1])[1]:
                points.append([float(critical_point.birth_time), float(critical_point.death_time)])

        for node in self.graphs[len(self.graphs) - 1].nodes:
            if node.critical_point.death_time is None:
                points.append([float(node.critical_point.birth_time), float(self.end_time)])

        self.diagram = points

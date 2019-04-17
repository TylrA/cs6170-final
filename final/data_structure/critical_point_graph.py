import numpy as np
import copy

squared_euclid_error = 100.0     # I.e., critical points at distance of 10 pixels from previous?

class CriticalPoint:
    def __init__(self, x, y, crit_type, birth_time):
        self.x = x                            # x coordinate, float
        self.y = y                            # y coordinate, float
        self.crit_type = crit_type            # critical point type, either 'max' or 'min', char[]
        self.birth_time = birth_time

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


class Graph:
    # Initialization requires at least one critical point
    def __init__(self, critical_point):
        self.nodes.append(Node(critical_point))

    # Critical points MUST be added by traversing the curve of the boundary
    def add_node(self, node):
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

    # Reduce noisy critical points. Keep older living critical points
    def smooth_bumps(self):
        changed_flag = True
        while changed_flag:
            changed_flag = False
            for i in range(0, len(self.nodes) - 1):
                if self.nodes[i] == self.nodes[i + 1]:
                    changed_flag = True
                    if self.nodes[i].birth_time < self.nodes[i + 1].birth_time:
                        self.delete_node(self.nodes[i + 1])
                    else:
                        self.delete_node(self.nodes[i])
                    break




    # This compares a previous time-step graph and returns critical points that were born and those that died
    def compare_with_previous_graph(self, previous_graph):
        critical_points_born = []
        critical_points_died = []

        # this part needs to be discussed more and finished maybe together?

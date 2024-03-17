import math
import visualizer
import numpy as np
from random import randint, randrange
counter = 0


class Vertex:
    def __init__(self, index, x, y):
        self.index = index
        self.x = x
        self.y = y
        self.available_vertices = []
        self.neighbours = []
        self.domain = []
        self.removed = []
        self.color = -1

    def calculate_distances(self, vertices):
        self.available_vertices = vertices[:]
        self.available_vertices.remove(self)
        self.available_vertices.sort(key=lambda o: self.distance(o))

    def get_nearest_vertex(self):
        return self.available_vertices.pop(0)

    def remove_vertex(self, vertex):
        self.available_vertices.remove(vertex)

    def __eq__(self, other):
        if not isinstance(other, Vertex):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f'{self.index} - ({self.x}, {self.y})'

    def distance(self, other):
        return math.sqrt(math.pow(self.x - other.x, 2) + math.pow(self.y - other.y, 2))

    def __hash__(self):
        return hash(self.x) ^ hash(self.y)


class Edge:
    def __init__(self, start_vertex, end_vertex):
        self.start_vertex = start_vertex
        self.end_vertex = end_vertex

    @staticmethod
    def calculate_orientation(a, b, c):
        value = ((c.y - a.y) * (b.x - a.x)) - ((b.y - a.y) * (c.x - a.x))
        return np.sign(value)

    @staticmethod
    def do_overlap(a, b, c):
        if b != a and b != c:
            return max(a.x, c.x) >= b.x >= min(a.x, c.x) and min(a.y, c.y) <= b.y <= max(a.y, c.y)
        return False

    def do_intersect(self, other):
        o1 = Edge.calculate_orientation(self.start_vertex, self.end_vertex, other.start_vertex)
        o2 = Edge.calculate_orientation(self.start_vertex, self.end_vertex, other.end_vertex)
        o3 = Edge.calculate_orientation(other.start_vertex, other.end_vertex, self.start_vertex)
        o4 = Edge.calculate_orientation(other.start_vertex, other.end_vertex, self.end_vertex)

        if o1 != o2 and o3 != o4 and (self.start_vertex != other.start_vertex and self.start_vertex != other.end_vertex
                                      and self.end_vertex != other.end_vertex and self.end_vertex != other.start_vertex):
            return True
        if o1 == 0 and Edge.do_overlap(self.start_vertex, other.start_vertex, self.end_vertex):
            return True
        if o2 == 0 and Edge.do_overlap(self.start_vertex, other.end_vertex, self.end_vertex):
            return True
        if o3 == 0 and Edge.do_overlap(other.start_vertex, self.start_vertex, other.end_vertex):
            return True
        if o4 == 0 and Edge.do_overlap(other.start_vertex, self.end_vertex, other.end_vertex):
            return True

        return False

    def __str__(self):
        return f'{self.start_vertex} -> {self.end_vertex}'


class Graph:
    def __init__(self, vertices):
        self.vertices = vertices
        self.edges = []
        self.adj_matrix = []
        for i in range(len(vertices)):
            self.adj_matrix.append([0] * len(vertices))

        self.solution = [-1] * len(vertices)
        self.counter = 0

    def add_edge(self, v1, v2):
        v1.neighbours.append(v2)
        v2.neighbours.append(v1)
        self.adj_matrix[v1.index][v2.index] = 1
        self.adj_matrix[v2.index][v1.index] = 1

    def generate_edges(self):
        edges = []
        vertices = self.vertices[:]
        while vertices:
            v1 = vertices[randrange(0, len(vertices))]
            if not v1.available_vertices:
                vertices.remove(v1)
                continue

            v2 = v1.get_nearest_vertex()
            v2.remove_vertex(v1)
            edge = Edge(v1, v2)
            if any(edge.do_intersect(e) for e in edges):
                continue

            edges.append(edge)
            self.add_edge(v1, v2)

        self.edges = edges

    def solve(self, number_of_colors, ac_3=True, lcv=True, mrv=True):
        for v in self.vertices:
            v.domain = [i for i in range(number_of_colors)]
        self.backtracking(0, 0, ac_3, lcv, mrv)
        if all(v.color != -1 for v in self.vertices):
            print('Solution found')
            visualizer.visualize_graph(self)
            print(self.counter)
        else:
            print('Solution not found')

    def solve_clear(self, number_of_colors):
        self.counter = 0
        self.color_graph(0, number_of_colors)
        if all(v.color != -1 for v in self.vertices):
            print('Solution found')
            print(self.counter)
        else:
            print('Solution not found')

    def is_safe(self, v, c):
        for i in range(len(self.vertices)):
            if self.adj_matrix[v.index][i] == 1 and c == self.vertices[i].color:
                return False

        return True

    def backtracking(self, index, visited, ac_3, lcv, mrv):
        self.counter += 1
        # if lcv:
        #     self.lcv(index)
        for color in self.vertices[index].domain:
            if self.is_safe(self.vertices[index], color):
                self.vertices[index].color = color
                if ac_3:
                    for v in self.vertices[index].neighbours:
                        if color in v.domain:
                            v.domain.remove(color)
                            v.removed.append(color)
                    # self.ac_3()
                # if index + 1 < len(self.vertices):
                if visited + 1 < len(self.vertices) and any(v.color == -1 for v in self.vertices):
                    if mrv:
                        index = self.get_next_mrv()
                    else:
                        index = visited + 1
                    solution = self.backtracking(index, visited + 1, ac_3, lcv, mrv)
                    if solution:
                        return True
                    else:
                        for v in self.vertices:
                            v.domain += v.removed
                            v.removed.clear()

        return False

    def color_graph(self, index, number_of_colors):
        self.counter += 1
        for color in range(number_of_colors):
            if self.is_safe(self.vertices[index], color):
                self.vertices[index].color = color
                if index + 1 < len(self.vertices):
                    self.color_graph(index + 1, number_of_colors)

        return

    def lcv(self, index):
        v = self.vertices[index]
        occurrences = []
        for color in v.domain:
            occ_counter = 0
            for n in v.neighbours:
                if color in n.domain:
                    occ_counter += 1
            occurrences.append((color, occ_counter))
        occurrences.sort(key=lambda x: x[1])
        v.domain = []
        for o in occurrences:
            v.domain.append(o[0])

    def get_next_mrv(self):
        choices = []
        for v in self.vertices:
            if v.color == -1:
                choices.append(v)

        min_v = choices[0]
        for v in choices[1:]:
            if len(v.domain) < len(min_v.domain):
                min_v = v
        return self.vertices.index(min_v)

    def ac_3(self):
        queue = []
        for v in self.vertices:
            for n in v.neighbours:
                queue.append((v, n))

        while queue:
            v1, v2 = queue.pop(0)
            if self.remove_consistent_values(v1, v2):
                for n in v1.neighbours:
                    queue.append((n, v1))

    @staticmethod
    def remove_consistent_values(v1, v2):
        if len(v2.domain) > 1:
            return False

        removed = False
        for color in v1.domain:
            if color in v2.domain:
                v1.domain.remove(color)
                v1.removed.append(color)
                removed = True
                break
        return removed

    def print_adj_matrix(self):
        for row in self.adj_matrix:
            print(row)

    def reset(self):
        for v in self.vertices:
            v.color = -1


class Plane:
    def __init__(self, len_x, len_y):
        self.len_x = len_x
        self.len_y = len_y
        self.graph_vertices = []

    def generate_graph_vertices(self, number_of_vertices):
        index = 0
        for i in range(number_of_vertices):
            v = Vertex(index, randint(0, self.len_x), randint(0, self.len_y))
            while v in self.graph_vertices:
                v = Vertex(index, randint(0, self.len_x), randint(0, self.len_y))

            self.graph_vertices.append(v)
            index += 1

    def save_points(self):
        with open('vertices.txt', 'w') as writer:
            for v in self.graph_vertices:
                writer.write(str(v.x) + ';' + str(v.y) + '\n')

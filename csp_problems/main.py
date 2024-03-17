from graph_coloring import *
from einstein import Solution
import time


def load_vertices(plane):
    with open('vertices.txt', 'r') as reader:
        index = 0
        for line in reader:
            data = [x.strip() for x in line.split(';')]
            v = Vertex(index, int(data[0]), int(data[1]))
            plane.graph_vertices.append(v)
            index += 1


def main():
    # plane = Plane(7, 7)
    # plane.generate_graph_vertices(40)
    #
    # for v in plane.graph_vertices:
    #     v.calculate_distances(plane.graph_vertices)
    # graph = Graph(plane.graph_vertices)
    # graph.generate_edges()
    # start = time.time()
    # graph.solve(4)
    # print(time.time() - start)

    s = Solution()
    start = time.time()
    s.solve_v2()
    print(time.time() - start)


if __name__ == '__main__':
    main()

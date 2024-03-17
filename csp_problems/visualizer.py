import matplotlib.pylab as plt

color_mapper = {
    0: 'red',
    1: 'blue',
    2: 'green',
    3: 'purple'
}


def visualize_graph(graph):
    for e in graph.edges:
        plt.plot([e.start_vertex.x, e.end_vertex.x], [e.start_vertex.y, e.end_vertex.y], color='gray')
    for vertex in graph.vertices:
        plt.plot([vertex.x], [vertex.y], marker='o', markersize=6, color=color_mapper[vertex.color])

    plt.show()

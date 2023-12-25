from aoc_common import get_puzzle_input, run, sprint
from aoc_common.benchmark import print_timings
import graphviz
import networkx as nx
from operator import mul

input_data = get_puzzle_input()


def load_input(input_data):
    components = {}
    for line in input_data:
        node, connections = line.split(":")
        connections = connections.split()
        components[node] = connections
    return components


def render_graph(components):
    graph = graphviz.Digraph()
    for node, connections in components.items():
        graph.node(node)
        for connection in connections:
            graph.edge(node, connection)
    return graph


@print_timings
def part_1():
    components = load_input(input_data)
    # graph = render_graph(components)
    # graph.render("day25")

    graph = nx.Graph()

    for node, connections in components.items():
        for connection in connections:
            graph.add_edge(node, connection)

    cuts = nx.minimum_edge_cut(graph)
    assert len(cuts) == 3
    graph.remove_edges_from(cuts)

    return mul(*[len(c) for c in nx.connected_components(graph)])
    # return list(nx.connected_components(graph))


@print_timings
def part_2():
    pass


run(part_1, part_2, __name__)

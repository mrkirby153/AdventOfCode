from aoc_common import get_puzzle_input, run, sprint
from aoc_common.benchmark import print_timings
from collections import deque
from math import lcm

input_data = get_puzzle_input()


def load_data(input_data):
    nodes = {}
    instructions = deque(input_data[0])
    for line in input_data[2:]:
        node, connections = line.split("=")
        node = node.strip()
        connections = connections.replace("(", "").replace(")", "").split(",")
        nodes[node] = list(map(str.strip, connections))
    return nodes, instructions


@print_timings
def part_1():
    nodes, instructions = load_data(input_data)
    sprint(nodes)
    sprint(instructions)

    current_node = "AAA"

    steps = 0
    while current_node != "ZZZ":
        instruction = instructions[0]
        instructions.rotate(-1)
        sprint("Instruction:", instruction, "Next instructions", instructions)

        node_set = nodes[current_node]
        current_node = node_set[0] if instruction == "L" else node_set[1]
        steps += 1
    return steps


def find_start_nodes(nodes):
    return [node for node in nodes if node[-1] == "A"]


def is_end_nodes(nodes):
    return all([node[-1] == "Z" for node in nodes])


def path_length_part_2(start, instructions, nodes):
    instructions = deque(instructions)

    current_node = start

    steps = 0
    while current_node[-1] != "Z":
        instruction = instructions[0]
        instructions.rotate(-1)
        node_set = nodes[current_node]
        current_node = node_set[0] if instruction == "L" else node_set[1]
        steps += 1
    return steps


@print_timings
def part_2():
    nodes, instructions = load_data(input_data)
    sprint(nodes)
    sprint(instructions)

    start_nodes = find_start_nodes(nodes)

    results = []
    for node in start_nodes:
        size = path_length_part_2(node, instructions, nodes)
        results.append(size)
    sprint(results)
    return lcm(*results)


run(part_1, part_2)

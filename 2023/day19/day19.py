from aoc_common import get_puzzle_input, run, sprint
from aoc_common.benchmark import print_timings
from collections import namedtuple, defaultdict
from copy import deepcopy
from aoc_common.io import numbers
import re
from tqdm import tqdm
from functools import reduce
from operator import mul

input_data = get_puzzle_input()

Workflow = namedtuple("Workflow", ["name", "steps"])
Part = namedtuple("Part", ["x", "m", "a", "s"])
Rule = namedtuple("Rule", ["rule", "destination"])

WORKFLOW_RE = re.compile(r"(\w+)\{(.*)\}")


def load_input(input_data):
    workflows = {}
    parts = []
    read_workflows = False

    def _parse_rule(rule):
        if ":" in rule:
            return Rule(*rule.split(":"))
        else:
            return Rule("True", rule)  # Always true

    def _parse_part(line):
        return Part(*numbers(line))

    def _parse_workflow(line):
        name, steps = WORKFLOW_RE.match(line).groups()
        return Workflow(name, [_parse_rule(rule) for rule in steps.split(",")])

    for line in input_data:
        if read_workflows:
            parts.append(_parse_part(line))
        elif line == "":
            read_workflows = True
        else:
            workflow = _parse_workflow(line)
            workflows[workflow.name] = workflow
    return parts, workflows


def eval_workflow(workflow, part):
    for rule in workflow.steps:
        if eval(rule.rule, {"x": part.x, "m": part.m, "a": part.a, "s": part.s}):
            return rule.destination
    return None


def run_part(part, workflows):
    sprint(f"Evaluating part {part}...")
    current = "in"
    while current != "A" and current != "R":
        sprint(f"Current: {current}")
        current = eval_workflow(workflows[current], part)
    if current == "A":
        return True
    elif current == "R":
        return False
    else:
        raise Exception("Invalid workflow termination")


def get_rating(part):
    return part.x + part.m + part.a + part.s


all_valid = []


def traverse_tree(workflows, current_node, ranges):
    if current_node == "A":
        sprint(f"Found accepted range: {ranges}")
        all_valid.append(ranges)
        return
    if current_node == "R":
        return

    for rule in workflows[current_node].steps:
        if rule.rule == "True":
            traverse_tree(workflows, rule.destination, deepcopy(ranges))
        else:
            variable = rule.rule[0]
            condition = rule.rule[1]
            constraint = int(rule.rule[2:])
            destination = rule.destination

            current = ranges[variable]

            lower = set(range(1, constraint + 1))
            higher = set(range(constraint, 4001))

            if condition == "<":
                new_field = current - higher  # Remove all higher values
            elif condition == ">":
                new_field = current - lower  # Remove all lower values

            ranges[variable] = (
                current - new_field
            )  # Anything not in new_field is invalid and should be passed on

            new_part = deepcopy(ranges)
            new_part[variable] = new_field
            ranges = deepcopy(ranges)

            traverse_tree(workflows, destination, new_part)


@print_timings
def part_1():
    parts, workflows = load_input(input_data)

    accepted = []
    rejected = []

    for part in tqdm(parts, desc="Parts"):
        to_append = accepted if run_part(part, workflows) else rejected
        to_append.append(part)

    sprint(f"Accepted: {accepted}")
    sprint(f"Rejected: {rejected}")

    return sum(get_rating(part) for part in accepted)


@print_timings
def part_2():
    _parts, workflows = load_input(input_data)

    ranges = {
        "x": set(range(1, 4001)),
        "m": set(range(1, 4001)),
        "a": set(range(1, 4001)),
        "s": set(range(1, 4001)),
    }
    traverse_tree(workflows, "in", ranges)

    r = 0
    for k in all_valid:
        r += reduce(mul, (len(v) for v in k.values()), 1)
    return r


run(part_1, part_2, __name__)

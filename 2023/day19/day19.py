from aoc_common import get_puzzle_input, run, sprint
from aoc_common.benchmark import print_timings
from collections import namedtuple
from aoc_common.io import numbers
import re
from tqdm import tqdm

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
    pass


run(part_1, part_2, __name__)

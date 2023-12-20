from aoc_common import get_puzzle_input, run, sprint
from aoc_common.benchmark import print_timings
from enum import Enum
from collections import namedtuple, defaultdict
from copy import deepcopy
from tqdm import tqdm


input_data = get_puzzle_input()


Module = namedtuple("Module", ["type", "outputs", "state"])


class ModuleType(Enum):
    BROADCAST = 1
    FLIP_FLOP = 2
    CONJUNCTION = 3


class PulseType(Enum):
    LOW = 1
    HIGH = 2


def load_input(input_data):
    modules = {}
    conjunction_inputs = {}
    for line in input_data:
        node_name, destinations = line.split(" -> ")
        node_name = node_name.strip()
        destinations = destinations.strip().split(", ")

        if node_name == "broadcaster":
            modules[node_name] = Module(ModuleType.BROADCAST, destinations, None)
        elif node_name.startswith("%"):
            modules[node_name[1:]] = Module(ModuleType.FLIP_FLOP, destinations, False)
        elif node_name.startswith("&"):
            modules[node_name[1:]] = Module(ModuleType.CONJUNCTION, destinations, {})
            conjunction_inputs[node_name[1:]] = []
        else:
            raise ValueError(f"Unknown node type: {node_name}")

    # Resolve conjunction inputs
    for name, module in modules.items():
        for destination in module.outputs:
            if destination in conjunction_inputs:
                conjunction_inputs[destination].append(name)

    for name, inputs in conjunction_inputs.items():
        existing_module = modules[name]
        modules[name] = Module(
            existing_module.type,
            existing_module.outputs,
            {n: PulseType.LOW for n in inputs},
        )

    return modules


def propogate_button_push(modules):
    modules = deepcopy(modules)
    low_pulses = 1
    high_pulses = 0

    queue = [("button", "broadcaster", PulseType.LOW)]

    def _send_pulses(source_module, pulse_type, destination_modules):
        nonlocal queue, low_pulses, high_pulses
        for destination in destination_modules:
            if pulse_type == PulseType.LOW:
                low_pulses += 1
            elif pulse_type == PulseType.HIGH:
                high_pulses += 1
            queue.append((source_module, destination, pulse_type))

    pulsed_rx = False

    while queue:
        # sprint("Queue:", queue)
        source_module_name, dest_module_name, pulse_type = queue.pop(0)
        sprint(source_module_name, "-", pulse_type, "->", dest_module_name)
        dest_module = modules.get(dest_module_name)

        if dest_module_name == "rx" and pulse_type == PulseType.LOW:
            pulsed_rx = True

        if not dest_module:
            continue

        if dest_module.type == ModuleType.BROADCAST:
            destinations = dest_module.outputs
            _send_pulses(dest_module_name, pulse_type, destinations)
        elif dest_module.type == ModuleType.FLIP_FLOP:
            state = dest_module.state
            if pulse_type == PulseType.HIGH:
                continue  # Ignore high pulses

            if state:
                # Was on, flip off
                modules[dest_module_name] = Module(
                    dest_module.type, dest_module.outputs, False
                )
                _send_pulses(dest_module_name, PulseType.LOW, dest_module.outputs)
            else:
                # Was off, flip on
                modules[dest_module_name] = Module(
                    dest_module.type, dest_module.outputs, True
                )
                _send_pulses(dest_module_name, PulseType.HIGH, dest_module.outputs)

        elif dest_module.type == ModuleType.CONJUNCTION:
            state = dest_module.state

            # Record the new state
            state = {**state, source_module_name: pulse_type}
            modules[dest_module_name] = Module(
                dest_module.type, dest_module.outputs, state
            )

            # Check if all the state is high
            if all(v == PulseType.HIGH for v in state.values()):
                _send_pulses(dest_module_name, PulseType.LOW, dest_module.outputs)
            else:
                _send_pulses(dest_module_name, PulseType.HIGH, dest_module.outputs)
        else:
            raise ValueError(f"Unknown module type: {dest_module.type}")
    return low_pulses, high_pulses, modules, pulsed_rx


def push_button_many_times(modules, times):
    modules = deepcopy(modules)
    low_pulses = 0
    high_pulses = 0
    for _ in tqdm(range(times)):
        low, high, modules, _ignored = propogate_button_push(modules)
        low_pulses += low
        high_pulses += high
    return low_pulses, high_pulses


def determine_min_presses(modules):
    modules = deepcopy(modules)
    for i in tqdm(range(1, 1000000000000)):
        low, high, modules, pulsed_rx = propogate_button_push(modules)
        if pulsed_rx:
            return i


@print_timings
def part_1():
    modules = load_input(input_data)
    low, high = push_button_many_times(modules, 1000)
    return low * high


@print_timings
def part_2():
    modules = load_input(input_data)
    return determine_min_presses(modules)


run(part_1, part_2, __name__)

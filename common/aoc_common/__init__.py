import argparse
from functools import cache

parser = argparse.ArgumentParser()
parser.add_argument(
    "--sample", "-s", help="Run with sample data", action="store_true", default=False
)
parser.add_argument("--file", "-f", help="Run against a specific input file")
parser.add_argument(
    "--one", "-1", help="Run only part 1", action="store_true", default=False
)
parser.add_argument(
    "--two", "-2", help="Run only part 2", action="store_true", default=False
)
parser.add_argument(
    "--verbose",
    "-v",
    help="Verbose output (sprint for real input)",
    action="store_true",
)
parser.add_argument("--quiet", "-q", help="Don't sprint ever", action="store_true")
parser.add_argument("--year", "-y", help="Year of the puzzle")
parser.add_argument("--day", "-d", help="Day of the puzzle")

parsed_args = parser.parse_args()

settings = {"year": None, "day": None}


def sprint(*args, **kwargs):
    """
    Print output only when running the sample
    """
    if parsed_args.quiet:
        return
    if parsed_args.sample or parsed_args.verbose:
        print(*args, **kwargs)


@cache
def get_puzzle_input():
    file_path = (
        f"{settings['year']}/day{settings['day']:02}" if settings["year"] else None
    )

    if parsed_args.file:
        file_name = parsed_args.file
    else:
        file_name = "input.txt" if not parsed_args.sample else "sample.txt"

    file = f"{file_path}/{file_name}" if file_path else file_name

    with open(file) as f:
        return [x.replace("\n", "") for x in f.readlines()]


def run(part_1, part_2):
    if __name__ != "__main__":
        return
    if not parsed_args.one and not parsed_args.two:
        print(f"Part 1: {part_1()}")
        print(f"Part 2: {part_2()}")
    elif parsed_args.one:
        print(f"Part 1: {part_1()}")
    elif parsed_args.two:
        print(f"Part 2: {part_2()}")

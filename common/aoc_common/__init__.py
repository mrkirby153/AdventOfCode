import argparse
from functools import cache

parser = argparse.ArgumentParser()
parser.add_argument('--sample', '-s', help='Run with sample data', action='store_true', default=False)
parser.add_argument('--file', '-f', help='Run against a specific input file')
parsed_args = parser.parse_args()

def sprint(*args, **kwargs):
    """
    Print output only when running the sample
    """
    if parsed_args.sample:
        print(*args, **kwargs)

@cache
def get_puzzle_input():
    if parsed_args.file:
        file_name = parsed_args.file
    else:
        file_name = 'input.txt' if not parsed_args.sample else 'sample.txt'
    with open(file_name) as f:
        return [x.replace('\n', '') for x in f.readlines()]
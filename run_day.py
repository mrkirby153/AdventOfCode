#!/bin/env python3
from aoc_common import parsed_args, settings
from importlib import import_module
import datetime
from pytz import timezone
from aocd.models import Puzzle


def get_year_and_day():
    year = (
        datetime.date.today().year
        if parsed_args.year is None
        else int(parsed_args.year)
    )
    if parsed_args.day is None:
        # Automatically determining day
        tz = timezone("EST")
        now = datetime.datetime.now(tz)
        day = now.day
        if day > 25:
            print("Could not automatically determine day. Is it after christmas?")
            exit(1)
    else:
        day = int(parsed_args.day)

    assert year >= 2023, "Year must be 2023 or later"
    assert day >= 1 and day <= 25, "Day must be between 1 and 25"
    return year, day


def main():
    year, day = get_year_and_day()
    settings["year"], settings["day"] = year, day
    module = import_module(
        f"{settings['year']}.day{settings['day']:02}.day{settings['day']:02}"
    )

    print(f"{year} - Day {day:02}\n")
    if not parsed_args.one and not parsed_args.two:
        print("Part 1:", module.part_1())
        print("Part 2:", module.part_2())
    elif parsed_args.one:
        print("Part 1:", module.part_1())
    elif parsed_args.two:
        print("Part 2:", module.part_2())


if __name__ == "__main__":
    main()

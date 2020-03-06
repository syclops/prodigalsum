"""
Calculate the sum of a range of integers and print the result.

Author: Steve Matsumoto <stephanos.matsumoto@sporic.me>
"""
import argparse
import sys

from builtin_range import BuiltinRange
from index_range import IndexRange
from list_range import ListRange


# Define constants used throughout the script.
BUILTIN = "builtin"
LIST = "list"
INDEX = "index"
RANGE_CONSTRUCTOR = {
    BUILTIN: BuiltinRange,
    INDEX: IndexRange,
    LIST: ListRange,
}


def get_parser(name):
    """
    Create and return an instance of the command-line argument parser for this
    script.

    Args:
        name: The name of the program (usually the script filename).

    Returns:
        An ArgumentParser instance that can parse the script's command-line
        arguments.
    """
    parser = argparse.ArgumentParser(name)
    parser.add_argument("--range-type", choices=[BUILTIN, LIST, INDEX],
                        default=BUILTIN,
                        help=f"type of range to use (default: {BUILTIN})")
    parser.add_argument("range_args", nargs="+", type=int,
                        help="arguments to pass to range (1-3 integers)")
    return parser


def main(args=sys.argv):
    """
    Run the main logic of the script.

    Args:
        args: The command-line arguments to pass to the script.

    Returns:
        None.
    """
    # Parse command-line arguments.
    parser = get_parser(args[0])
    parsed_args = parser.parse_args(args[1:])

    # Create range instantiation (including start, stop, and step parameters)
    # based on command-line options.
    range_object = RANGE_CONSTRUCTOR[parsed_args.range_type](
        *parsed_args.range_args)

    gauss_sum = 0
    while not range_object.done():
        gauss_sum += range_object.value()
        range_object.next()
    print(f"The sum of the integer range is {gauss_sum}")


if __name__ == '__main__':
    main()

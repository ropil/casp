#!/usr/bin/env python3


# Library functions


# Main; for callable scripts
def main():
    from argparse import ArgumentParser
    from sys import argv, stdin
    parser = ArgumentParser(
        description="This is a stub file.")
    parser.add_argument(
        "-a", action="store_true", default=False, help="Prints nothing")
    parser.add_argument(
        "-t", nargs=1, default=["nothing"], metavar="TEXT",
        help="What to print")
    parser.add_argument(
        "files", nargs="*", metavar="FILE", help="Files for input")
    arguments = parser.parse_args(argv[1:])
    files = arguments.files
    # Use stdin if no supplied files
    if len(arguments.files) == 0:
        files = [stdin]

    # Set variables here

    # Parse STDIN or files
    for f in files:
        infile = f
        # Open for reading if file path specified
        if isinstance(f, str):
            infile = open(f, 'r')
        for line in infile:
            print(line)
        infile.close()


if __name__ == '__main__':
    main()
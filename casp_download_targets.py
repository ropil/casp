#!/usr/bin/env python3
from os import listdir
from os.path import isfile, join
from re import compile
from urllib.request import urlopen
from bs4 import BeautifulSoup


# Library functions
def find_targets_new(url, target_regex, targets_downloaded=None):
    # Initialize a new targets downloaded if none is provided
    if targets_downloaded is None:
        targets_downloaded = {}

    new_targets = {}

    # Get and read the text from the webpage
    with urlopen(url) as webpage:
        download_area = webpage.read()

    soup = BeautifulSoup(download_area, 'html.parser')
    targets = soup.find_all("a", string=target_regex)

    for target in targets:
        if not target.string in targets_downloaded:
            print(target.string)
            new_targets[target.string] = url + "/" + target.string

    return new_targets


def find_targets_downloaded(directory, target_regex):
    targets_downloaded = {}
    for target in listdir(directory):
        target_path = join(directory, target)
        if isfile(join(directory, target)):
            print("Found target " + target + " with path " + target_path)
            targets_downloaded[target] = target_path
    return targets_downloaded


def download_targets(new_targets, destination):
    # Print what is happening
    for target in new_targets:
        print("\t".join(["Downloading", target, "from", new_targets[target]]))


# Main; for callable scripts
def main():
    from argparse import ArgumentParser
    from sys import argv, stdin
    parser = ArgumentParser(
        description="Download CASP12 targets.")
    parser.add_argument(
        "-a", action="store_true", default=False, help="Prints nothing")
    parser.add_argument(
        "-url", nargs=1, default=["http://predictioncenter.org/download_area/CASP12/server_predictions/"],
        metavar="URL", help="CASP download area directory, " +
                            "default=http://predictioncenter.org/download_area/CASP12/server_predictions/")
    parser.add_argument(
        "-regex", nargs=1, default=[".*\.stage2.*\.srv\.tar\.gz"],
        metavar="REGEX", help="Target regex, default='.*\.stage2.*\.srv\.tar\.gz'")
    parser.add_argument(
        "-dest", nargs=1, default=[None],
        metavar="DIR", help="Target download destination directory, default=first in list")
    parser.add_argument(
        "directories", nargs="*", metavar="DIR", help="Directories where to download targets")
    arguments = parser.parse_args(argv[1:])
    directories = arguments.directories
    # Use stdin if no supplied directories
    if len(directories) == 0:
        directories = stdin

    # Set variables here
    target_regex = compile(arguments.regex[0])
    url = arguments.url[0]
    destination = arguments.dest[0]
    targets_downloaded = {}

    # Find targets in directories
    for d in directories:
        infile = d
        # find directory targets contents
        if isinstance(d, str):
            if destination is None:
                print("Setting destination directory to " + d)
                destination = d
            print("Parse content in directory " + d)
            # and join all found in different directories; avoiding duplicates
            targets_downloaded = {**targets_downloaded, **find_targets_downloaded(d, target_regex)}

    # Get all new target urls
    new_targets = find_targets_new(url, target_regex, targets_downloaded)

    # Download the targets
    download_targets(new_targets, destination)

if __name__ == '__main__':
    main()
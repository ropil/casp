#!/usr/bin/env python3
from os import listdir
from os.path import isfile, join
from re import compile
from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup

'''
 {casp_download_targets is a shell utility to download CASP targets from the online download area.}
 Copyright (C) 2017  Robert Pilstål

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program. If not, see <http://www.gnu.org/licenses/>.
'''


# Version and license information
def get_version_str():
    return "\n".join([
        "casp_download_targets  Copyright (C) 2017  Robert Pilstål;",
        "This program comes with ABSOLUTELY NO WARRANTY.",
        "This is free software, and you are welcome to redistribute it",
        "under certain conditions; see supplied General Public License."
        ])


# Library functions
def find_targets_new(url, target_regex, targets_downloaded=None, verbose=False):
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
            if verbose:
                print(target.string)
            new_targets[target.string] = url + "/" + target.string

    return new_targets


def find_targets_downloaded(directory, target_regex, verbose=False):
    targets_downloaded = {}
    # Check all files in directory
    for target in listdir(directory):
        # Only consider files matching target regex
        if target_regex.match(target):
            target_path = join(directory, target)
            if isfile(join(directory, target)):
                if verbose:
                    print("Found target " + target + " with path " + target_path)
                targets_downloaded[target] = target_path
    return targets_downloaded


def download_targets(new_targets, destination, verbose=False):
    # Print what is happening
    for target in new_targets:
        download_path = destination + "/" + target
        if verbose:
            print("\t".join(["Downloading", target, "from", new_targets[target], "->", download_path ]))
        urlretrieve(new_targets[target], download_path)


# Main; for callable scripts
def main():
    from argparse import ArgumentParser
    from sys import argv, stdin
    parser = ArgumentParser(
        description="Utility to download CASP targets from the online download area.")
    parser.add_argument(
        "-verbose", action="store_true", default=False, help="Be verbose, default=silent")
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
    parser.add_argument('-v', '--version', action='version', version=get_version_str())
    parser.add_argument(
        "directories", nargs="*", metavar="DIR", help="Directories where to download targets")
    arguments = parser.parse_args(argv[1:])
    directories = arguments.directories
    # Use stdin if no supplied directories
    if len(directories) == 0:
        directories = stdin

    # Set variables here
    verbose = arguments.verbose
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
                if verbose:
                    print("Setting destination directory to " + d)
                destination = d
            if verbose:
                print("Parse content in directory " + d)
            # and join all found in different directories; avoiding duplicates
            targets_downloaded = {**targets_downloaded, **find_targets_downloaded(d, target_regex, verbose=verbose)}

    # Get all new target urls
    new_targets = find_targets_new(url, target_regex, targets_downloaded, verbose=verbose)

    # Download the targets
    download_targets(new_targets, destination, verbose=verbose)

if __name__ == '__main__':
    main()
#!/bin/env python3
# -*- coding: utf-8 -*-

'''

Copyright (C) 2020 Tommy Lau <http://tommy.net.cn/>

https://github.com/TommyLau/actions-openwrt
Description: Build OpenWrt image with GitHub Actions

'''

from argparse import ArgumentParser, FileType, RawTextHelpFormatter
from construct import *

VERSION = "v0.1.0"
DESCRIPTION = "A ZTE Optical Modem Configuration Tool"
DOCUMENTS = """
Copyright (C) 2020 Tommy Lau <http://tommy.net.cn/>
"""


def main():
    parser = ArgumentParser(prog='ztecfg', description=DESCRIPTION, epilog=DOCUMENTS,
                            formatter_class=RawTextHelpFormatter)
    group = parser.add_mutually_exclusive_group()
    parser.add_argument('-v', '--version', action='version', version='ztecfg {}'.format(VERSION))
    group.add_argument('-u', '--unpack', nargs=1, type=FileType('rb'), help='unpack ZTE config file')
    group.add_argument('-p', '--pack', nargs=2, type=FileType('rb'), help='pack ZTE config file')
    parser.add_argument('-o', '--output', nargs=1, type=FileType('wb'), help='specific output filename')

    # Exit if nothing to do
    if not args.unpack and not args.pack:
        parser.print_help()
        return 0

    if args.unpack:
        print('unpack')

    if args.pack:
        print('pack')


if __name__ == "__main__":
    main()

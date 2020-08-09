#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''

Copyright (C) 2020 Tommy Lau <http://tommy.net.cn/>

https://github.com/TommyLau/ztecfg
Description: A ZTE Optical Modem Configuration Tool

'''

from argparse import ArgumentParser, FileType, RawTextHelpFormatter
from construct import *
import os

VERSION = 'v0.1.0'
DESCRIPTION = 'A ZTE Optical Modem Configuration Tool'
DOCUMENTS = '''
Copyright (C) 2020 Tommy Lau <http://tommy.net.cn/>
'''

file_header = Struct(
    'magic' / Const(b'\x99\x99\x99\x99DDDDUUUU\xaa\xaa\xaa\xaa'),
    'unknow1' / Array(2, Int32ub),
    'sign1' / Int32ub,
    'unknow2' / Array(8, Int32ub),
    'sign2' / Int32ub,
    'sign3' / Int32ub,
    'header_size' / Int32ub,
    'content_size' / Int32ub,
    'unknow3' / Array(13, Int32ub)
)

device_header = Struct(
    'magic' / Const(b'\x04\x03\x02\x01'),
    'unknown1' / Int32ub,
    'name_length' / Int32ub,
)

block_header = Struct(
    'magic' / Const(b'\x01\x02\x03\x04'),
    'unknown1' / Int32ub,
    'size' / Int32ub,
    'compressed_size' / Int32ub,
    'block_size' / Int32ub,
    'compressed_crc32' / Int32ub,
    'header_crc32' / Int32ub,
    'unknown2' / Array(8, Int32ub),
)

block = Struct(
    'size' / Int32ub,
    'compressed_size' / Int32ub,
    'offset' / Int32ub,
    'content' / Bytes(this.compressed_size),
)

cfg_header = Struct(
    'file_header' / file_header,
    'device_header' / device_header,
    'device_name' / Bytes(this.device_header.name_length),
)


def get_new_filename(original, extension):
    return os.path.splitext(original)[0] + '.' + extension


def unpack(cfg_file, xml_filename):
    pass


def main():
    parser = ArgumentParser(prog='ztecfg', description=DESCRIPTION, epilog=DOCUMENTS,
                            formatter_class=RawTextHelpFormatter)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-u', '--unpack', nargs=1, type=FileType('rb'),
                       help='unpack ZTE config file',
                       metavar='cfg_file')
    group.add_argument('-p', '--pack', nargs=2, type=FileType('rb'),
                       help='pack ZTE config file',
                       metavar=('cfg_file', 'xml_file'))
    parser.add_argument('-o', '--output', help='specific output filename', metavar='file')
    parser.add_argument('-f', '--force', action='store_true', help='force to overwrite output file')
    parser.add_argument('-v', '--version', action='version', version=f'ztecfg {VERSION}')
    args = parser.parse_args()

    # Display help if nothing to do
    if not args.unpack and not args.pack:
        parser.print_help()
        return 0

    if args.output:
        filename = args.output
    elif args.unpack:
        filename = get_new_filename(args.unpack[0].name, 'xml')
    elif args.pack:
        filename = args.pack[1].name + '.cfg'
    else:
        parser.print_help()
        return

    if os.path.exists(filename) and not args.force:
        print(f'File "{filename}" exists, use "--force" option if you want to overwrite the output file.')
        return

    if args.unpack:
        print('unpack')
        unpack(args.unpack[0], filename)
        return

    if args.pack:
        print('pack')
        return


if __name__ == "__main__":
    main()

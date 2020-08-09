#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''

Copyright (C) 2020 Tommy Lau <http://tommy.net.cn/>

https://github.com/TommyLau/ztecfg
Description: A ZTE Optical Modem Configuration Tool

'''

from argparse import *
from construct import *
from zlib import *
import os

VERSION = 'v0.1.0'
DESCRIPTION = 'A ZTE Optical Modem Configuration Tool'
DOCUMENTS = '''
(i) Project page: https://github.com/TommyLau/ztecfg
(?) Bug report: https://github.com/TommyLau/ztecfg/issues

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
    # Get cfg file content
    file_content = cfg_file.read()
    cfg_file.close()

    # Parse cfg file header
    cfg = cfg_header.parse(file_content)
    print(f"\nDevice name: {cfg.device_name.decode('utf-8')}\n")

    # The offset of blocks
    offset = file_header.sizeof() + device_header.sizeof() + cfg.device_header.name_length

    # Get blocks
    blocks = file_content[offset:]

    # Parse block header
    header = block_header.parse(blocks)

    # New offset for block content
    offset = block_header.sizeof()

    xml = b''
    compressed_data = b''
    i = 1

    while True:
        # Parse each block
        b = block.parse(blocks[offset:])

        # Display process information
        print(f'Block {i}: size={b.size}, compressed={b.compressed_size}, offset={b.offset}')
        i += 1

        # Point to next block
        offset = b.offset

        # Append to XML output
        xml += decompress(b.content)

        # Compressed data for crc32 checksum
        compressed_data += b.content

        # No more blocks
        if offset == 0:
            break

    # Checksum for compressed data
    crc = crc32(compressed_data)
    if header.compressed_crc32 != crc:
        print('Checksum fail for compressed data, please make sure cfg file is valid.')
        return

    # Checksum for block header
    crc = crc32(block_header.build(header)[:24])
    if header.header_crc32 != crc:
        print('Checksum fail for block header, please make sure cfg file is valid.')
        return

    # Write XML content to file
    print(f'\nWrite XML output to file "{xml_filename}"\n')
    with open(xml_filename, 'wb') as f:
        f.write(xml)

    return


def pack(cfg_file, xml_file, cfg_filename):
    # Get cfg file content
    file_content = cfg_file.read()
    cfg_file.close()

    # Parse cfg file header
    cfg = cfg_header.parse(file_content)
    print(f"\nDevice name: {cfg.device_name.decode('utf-8')}\n")

    # Get XML content
    xml = xml_file.read()
    xml_file.close()

    # The offset of blocks
    offset = file_header.sizeof() + device_header.sizeof() + cfg.device_header.name_length

    # Get blocks
    blocks = file_content[offset:]

    # Parse block header
    header = block_header.parse(blocks)

    compressed_data = b''
    file_content = b''
    offset = block_header.sizeof()
    length = len(xml)
    i = 0

    while True:
        offset1 = i * header.block_size
        offset2 = (i + 1) * header.block_size

        if offset2 > length:
            offset2 = length
            block_size = offset2 - offset1
        else:
            block_size = header.block_size

        # Build block
        content = compress(xml[offset1:offset2], Z_BEST_COMPRESSION)
        compressed_data += content
        size = block_size
        compressed_size = len(content)
        offset = offset + 12 + compressed_size

        if offset2 == length:
            offset = 0

        # Display process information
        i += 1
        print(f'Block {i}: size={size}, compressed={compressed_size}, offset={offset}')

        # Append compressed data
        file_content += block.build(dict(size=size, compressed_size=compressed_size, offset=offset, content=content))

        # No more data to process
        if offset == 0:
            break

    # Build block header
    header.size = len(xml)
    header.compressed_size = block_header.sizeof() + len(file_content)
    header.compressed_crc32 = crc32(compressed_data)
    header.header_crc32 = crc32(block_header.build(header)[:24])

    # Build cfg header
    cfg.file_header.content_size = device_header.sizeof() + cfg.device_header.name_length + block_header.sizeof() + len(
        file_content)
    cfg_content = cfg_header.build(cfg) + block_header.build(header) + file_content

    # Write cfg content to file
    print(f'\nWrite CFG output to file "{cfg_filename}"\n')
    with open(cfg_filename, 'wb') as f:
        f.write(cfg_content)

    return


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
        unpack(args.unpack[0], filename)
        return

    if args.pack:
        pack(args.pack[0], args.pack[1], filename)
        return


if __name__ == "__main__":
    main()

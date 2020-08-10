# ztecfg

> A ZTE Optical Modem Configuration Tool

![GitHub Actions](https://github.com/TommyLau/ztecfg/workflows/Release%20ztecfg/badge.svg)

## Usage

```bash
usage: ztecfg [-h] [-u cfg_file | -p cfg_file xml_file] [-o file] [-f] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -u cfg_file, --unpack cfg_file
                        unpack ZTE config file
  -p cfg_file xml_file, --pack cfg_file xml_file
                        pack ZTE config file
  -o file, --output file
                        specific output filename
  -f, --force           force to overwrite output file
  -v, --version         show program's version number and exit
```

### Unpack

Unpack a ZTE cfg file:

```bash
$ ./ztecfg -u ctce8_F663N.cfg
Write XML output to file "ctce8_F663N.xml"
```

Unpack a ZTE cfg file to specific file `out.xml`:

```bash
$ ./ztecfg -u ctce8_F663N.cfg -o out.xml
Write XML output to file "out.xml"
```

### Pack

Pack to ZTE cfg file with original cfg file and xml file:

```bash
$ ./ztecfg -p ctce8_F663N.cfg new.xml
Write CFG output to file "new.xml.cfg"
```

Pack ZTE cfg with a specific output file named `out.cfg`:

```bash
$ ./ztecfg -p ctce8_F663N.cfg new.xml -o out.cfg
Write CFG output to file "out.cfg"
```

## Warning

The unpack process will check the CRC checksum of both the file header and the block header to make sure the cfg file
is valid. Also the pack process will write back the checksum to the cfg file.

If the cfg file cannot be unpacked, it might indicate that the cfg file is incompatible with this tool. Under such
circumstances, please **DO NOT** try to pack it back, cause it might brick your optical modem.

Always backup your configurations before you do any modifications to your modem.

This tools had been tested only on `ZTE ZXHN F663N`, but it should be working on any `ZTE ZXHN` series optical modems
with a cfg backup file.

Use at your own risk, the author will not take any responsibilities of the damage to your devices.

## Special Thanks

- [中兴光猫系列配置解密工具](https://github.com/wx1183618058/ZET-Optical-Network-Terminal-Decoder)

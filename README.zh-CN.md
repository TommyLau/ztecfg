<div align="right">
  语言：
  <a title="英语" href="README.md">🇺🇸</a>
  🇨🇳
</div>

# ztecfg

> 中兴光猫配置文件修改工具

[![GitHub Actions](https://github.com/TommyLau/ztecfg/workflows/Release/badge.svg)](https://github.com/TommyLau/ztecfg/actions?query=workflow%3A%22Release%22)
[![GitHub Actions](https://github.com/TommyLau/ztecfg/workflows/Development/badge.svg)](https://github.com/TommyLau/ztecfg/actions?query=workflow%3A%22Development%22)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

## 使用说明

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

### 解包

解包一个 cfg 文件：

```bash
$ ./ztecfg -u ctce8_F663N.cfg
Write XML output to file "ctce8_F663N.xml"
```

解包一个 cfg 文件，并指定输出文件为 `out.xml`：

```bash
$ ./ztecfg -u ctce8_F663N.cfg -o out.xml
Write XML output to file "out.xml"
```

### 打包

使用原始的 cfg 文件和 xml 文件打包中兴 cfg 文件：

```bash
$ ./ztecfg -p ctce8_F663N.cfg new.xml
Write CFG output to file "new.xml.cfg"
```

打包中兴 cfg 文件，并指定输出文件为 `out.cfg`：

```bash
$ ./ztecfg -p ctce8_F663N.cfg new.xml -o out.cfg
Write CFG output to file "out.cfg"
```

## 警告

在解包的过程中，程序会检查文件头和文件块的 CRC 校验，以判断 cfg 文件是否有效。同样在打包 cfg 文件的过程中，本程序也会写入相应的校验值。

如果无法正常解包 cfg 文件，很有可能本工具无法处理该 cfg 文件。在这种情况下，请**不要**尝试重新打包，否则可能导致你的光猫变砖。

在对光猫进行任何操作和修改前，请务必进行备份。

本工具仅在`中兴 ZXHN F663N` 上测试通过，理论上可以支持所有`中兴 ZXHN` 系列的光猫 cfg 配置文件。

请您自行承担使用风险，作者对于您设备可能造成的损坏不承担任何责任。

## 特别感谢

- [中兴光猫系列配置解密工具](https://github.com/wx1183618058/ZET-Optical-Network-Terminal-Decoder)

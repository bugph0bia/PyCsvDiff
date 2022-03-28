PyCsvDiff
===
![Software Version](http://img.shields.io/badge/Version-v0.1.0-green.svg?style=flat)
[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)

## Overview
Output diff in CSV files.

## Version
v0.1.0

## Requirements
Python 3 (Use only Standard Library)  

## Usage
```
$python csvdiff.py -h
usage: csvdiff.py [-h] [-e ENCODING] [-p PRIMARYKEY] [-t] [--hide-index] [--hide-keyname] [--hide-value] csv1 csv2

Output the difference between two CSV files.

positional arguments:
  csv1                  1st CSV file.
  csv2                  2nd CSV file.

optional arguments:
  -h, --help            show this help message and exit
  -e ENCODING, --encoding ENCODING
                        Encoding for CSV files. (default: utf-8)
  -p PRIMARYKEY, --primarykey PRIMARYKEY
                        Column number as primary key. (range: 1-N, default: 1)
  -t, --has-title       Treat the first line as a header.
  --hide-index          Do not print row/column indexes.
  --hide-keyname        Do not print row/column key names.
  --hide-value          Do not print difference values.
```

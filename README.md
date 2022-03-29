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
usage: csvdiff.py [-h] [-e ENCODING] [-p PRIMARY_KEY] [-t] [--excel-style] [--hide-address] [--hide-keyname]
                  [--hide-value]
                  csv1 csv2

Output the difference between two CSV files.

positional arguments:
  csv1                  1st CSV file.
  csv2                  2nd CSV file.

optional arguments:
  -h, --help            show this help message and exit
  -e ENCODING, --encoding ENCODING
                        Encoding for CSV files. (default: utf-8)
  -p PRIMARY_KEY, --primary-key PRIMARY_KEY
                        Column number as primary key. (range: 1-N, default: 1)
  -t, --has-title       Treat the first line as a header.
  --excel-style         Print addresses excel A1 style.
  --hide-address        Do not print row/column addresses.
  --hide-keyname        Do not print row/column key names.
  --hide-value          Do not print difference values.
```

## Example
### Sample CSV Files
a.csv  
```
column1,column2,column3
aaa,1,1,1
ccc,3,3,3
ddd,4,4,4
```

b.csv  
```
column1,column2,column3
aaa,1,1,1
bbb,2,2,2
ddd,5,6,7
```

### Result example
Simple  
```
$ python csvdiff.py a.csv b.csv
+ [R2] > bbb,2,2,2
- [R2] > ccc,3,3,3
! [R4,C2 | R4,C2] [ddd,] > 4 | 5
! [R4,C3 | R4,C3] [ddd,] > 4 | 6
! [R4,C4 | R4,C4] [ddd,] > 4 | 7
(diff count: 5)
```

Handling header row  
```
$ python csvdiff.py a.csv b.csv -t
+ [R2] > bbb,2,2,2
- [R2] > ccc,3,3,3
! [R3,C2 | R3,C2] [ddd,column2] > 4 | 5
! [R3,C3 | R3,C3] [ddd,column3] > 4 | 6
! [R3,C4 | R3,C4] [ddd,] > 4 | 7
(diff count: 5)
```

Print addresses excel A1 style
```
$ python csvdiff.py a.csv b.csv -t --excel-style
+ [2:2] > bbb,2,2,2
- [2:2] > ccc,3,3,3
! [B3 | B3] [ddd,column2] > 4 | 5
! [C3 | C3] [ddd,column3] > 4 | 6
! [D3 | D3] [ddd,] > 4 | 7
(diff count: 5)
```

Hide addresses  
```
$ python csvdiff.py a.csv b.csv -t --hide-address
+ > bbb,2,2,2
- > ccc,3,3,3
! [ddd,column2] > 4 | 5
! [ddd,column3] > 4 | 6
! [ddd,] > 4 | 7
(diff count: 5)
```

Hide key names  
```
$ python csvdiff.py a.csv b.csv -t --hide-keyname
+ [R2] > bbb,2,2,2
- [R2] > ccc,3,3,3
! [R3,C2 | R3,C2] > 4 | 5
! [R3,C3 | R3,C3] > 4 | 6
! [R3,C4 | R3,C4] > 4 | 7
(diff count: 5)
```

Hide values  
```
$ python csvdiff.py a.csv b.csv -t --hide-value
+ [R2]
- [R2]
! [R3,C2 | R3,C2] [ddd,column2]
! [R3,C3 | R3,C3] [ddd,column3]
! [R3,C4 | R3,C4] [ddd,]
(diff count: 5)
```

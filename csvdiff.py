import sys
import csv
import argparse
from collections import namedtuple


# diff info
DiffInfo = namedtuple('DiffInfo', [
    'mark',  # diff kind (!, -, +)
    'address',  # row/column addresses of diff
    'keyname',  # row/column key names of diff
    'value',  # values of diff
])


def main():
    """main"""
    parser = argparse.ArgumentParser(description='Output the difference between two CSV files.')
    parser.add_argument('csv1', help='1st CSV file.')
    parser.add_argument('csv2', help='2nd CSV file.')
    parser.add_argument('-e', '--encoding', default='utf-8', help='Encoding for CSV files. (default: utf-8)')
    parser.add_argument('-p', '--primary-key', type=int, default=1, help='Column number as primary key. (range: 1-N, default: 1)')
    parser.add_argument('-t', '--has-title', action='store_true', help='Treat the first line as a header.')
    parser.add_argument('--excel-style', action='store_true', help='Print addresses excel A1 style.')
    parser.add_argument('--hide-address', action='store_true', help='Do not print row/column addresses.')
    parser.add_argument('--hide-keyname', action='store_true', help='Do not print row/column key names.')
    parser.add_argument('--hide-value', action='store_true', help='Do not print difference values.')
    args = parser.parse_args()

    # read csv
    csv1, header1 = read_csv(args.csv1, args.encoding, args.has_title)
    csv2, header2 = read_csv(args.csv2, args.encoding, args.has_title)

    # check column count
    if len(header1) != len(header2):
        print(f'error: different column count in CSV files. (csv1:{len(header1)}, csv2:{len(header2)})', file=sys.stderr)
        return

    # check primary key value
    if not (0 < args.primary_key <= len(header1)):
        print(f'error: primary key invalid. (primary key:{args.primary_key}, column count:{len(header1)})', file=sys.stderr)
        return

    # correct column number to start with 0
    primary_key = args.primary_key - 1

    # sort by primary key
    csv1.sort(key=lambda x: x[primary_key])
    csv2.sort(key=lambda x: x[primary_key])

    # get diff info
    diffs = diff_csv(csv1, header1, csv2, header2, primary_key, args.excel_style)
    # print result
    print_diffs(diffs, args.hide_address, args.hide_keyname, args.hide_value)


def read_csv(fname: str, encoding: str, has_header: bool):
    """Read CSV file

    Args:
        fname (str): CSV file.
        encoding (str): encoding for CSV File.
        has_header (bool): if first row is header then True, else False.

    Returns:
        tuple[list[list[str]], list[str]]: Tuple of CSV data and CSV header.
    """
    with open(fname, 'r', encoding=encoding) as f:
        csvdata = list(csv.reader(f))

    # Match the column count to their max
    max_colmuns = max(map(lambda x: len(x), csvdata))
    for row in csvdata:
        row.extend([''] * (max_colmuns - len(row)))

    # get header row
    if has_header:
        header = csvdata[0]
        csvdata = csvdata[1:]
    else:
        header = [''] * len(csvdata[0])

    return csvdata, header


def diff_csv(csv1: list[list[str]], header1: list[str],
             csv2: list[list[str]], header2: list[str],
             primary_key: int, excel_style: bool):
    """Diff CSV files.

    Args:
        csv1 (list[list[str]]): 1st CSV data.
        header1 (list[str]): 1st CSV header.
        csv2 (list[list[str]]): 2nd CSV data.
        header2 (list[str]): 2nd CSV header.
        primary_key (int): column number of primary key.
        excel_style (bool): excel A1 style.

    Returns:
        list[DiffInfo]: list of diff infos.
    """
    diffs = []

    ri1 = ri2 = 0
    while True:
        # get target row
        row1 = csv1[ri1] if len(csv1) > ri1 else None
        row2 = csv2[ri2] if len(csv2) > ri2 else None
        # get primary key of target row
        pkey1 = row1[primary_key] if row1 else None
        pkey2 = row2[primary_key] if row2 else None

        # exit when both CSV data is terminated
        if row1 is None and pkey2 is None:
            break

        # remaining lines of csv2, if csv1 is terminated
        # (== the row in csv2 only)
        elif pkey1 is None:
            diffs.append(DiffInfo(
                mark='+',
                address=make_row_address(ri2, excel_style),
                keyname='',
                value=','.join(row2),
            ))
            ri2 += 1

        # remaining lines of csv1, if csv2 is terminated
        # (== the row in csv1 only)
        elif pkey2 is None:
            diffs.append(DiffInfo(
                mark='-',
                address=make_row_address(ri1, excel_style),
                keyname='',
                value=','.join(row1),
            ))
            ri1 += 1

        # the row in csv2 only
        elif pkey1 > pkey2:
            diffs.append(DiffInfo(
                mark='+',
                address=make_row_address(ri2, excel_style),
                keyname='',
                value=','.join(row2),
            ))
            ri2 += 1

        # the row in csv1 only
        elif pkey1 < pkey2:
            diffs.append(DiffInfo(
                mark='-',
                address=make_row_address(ri1, excel_style),
                keyname='',
                value=','.join(row1),
            ))
            ri1 += 1

        # the row in both files
        else:  # pkey1 == pkey2
            for ci, (v1, v2) in enumerate(zip(row1, row2)):
                if v1 != v2:
                    diffs.append(DiffInfo(
                        mark='!',
                        address=make_cell_address(ri1, ri2, ci, excel_style),
                        keyname=f'{pkey1},{header1[ci]}',
                        value=f'{v1} | {v2}',
                    ))
            ri1 += 1
            ri2 += 1

    return diffs


def a1_address(ri, ci):
    """Make Excel A1 style address from row/column address."""
    CHR_A = 65  # ascii code of 'A'
    ALNUM = 26  # number of alphabet
    if ci >= ALNUM:
        return chr(CHR_A + (ci // ALNUM)) + chr(CHR_A + (ci % ALNUM)) + str(ri+1)
    else:
        return chr(CHR_A + (ci % ALNUM)) + str(ri+1)


def make_row_address(ri, excel_style):
    """Make row address for print."""
    if excel_style:
        return f'{ri+1}:{ri+1}'
    else:
        return f'R{ri+1}'


def make_cell_address(ri1, ri2, ci, excel_style):
    """Make cell addresses for print."""
    if excel_style:
        return f'{a1_address(ri1, ci)} | {a1_address(ri2, ci)}'
    else:
        return f'R{ri1+1},C{ci+1} | R{ri2+1},C{ci+1}'


def print_diffs(diffs, hide_address, hide_keyname, hide_value):
    """Print diffs.

    Args:
        diffs (list[DiffInfo]): list of diff infos.
        hide_address (bool): if true then do not print addresses.
        hide_keyname (bool): if true then do not print key names.
        hide_value (bool): if true then do not print values.
    """

    for diff in diffs:
        pstr = f'{diff.mark} '
        if not hide_address and diff.address:
            pstr += f'[{diff.address}] '
        if not hide_keyname and diff.keyname:
            pstr += f'[{diff.keyname}] '
        if not hide_value and diff.value:
            pstr += f'> {diff.value}'
        print(pstr)
    print(f'(diff count: {len(diffs)})')


if __name__ == '__main__':
    main()

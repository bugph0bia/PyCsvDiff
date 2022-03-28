import csv
import argparse
from collections import namedtuple


# diff info
DiffInfo = namedtuple('DiffInfo', [
    # diff kind (!, -, +)
    'mark',
    # row/column indexes of diff
    'index',
    # row/column key names of diff
    'keyname',
    # values of diff
    'value',
])


def main():
    """main"""
    parser = argparse.ArgumentParser(description='Output the difference between two CSV files.')
    parser.add_argument('csv1', help='1st CSV file.')
    parser.add_argument('csv2', help='2nd CSV file.')
    parser.add_argument('-e', '--encoding', default='utf-8', help='Encoding for CSV files. (default: utf-8)')
    parser.add_argument('-p', '--primarykey', type=int, default=1, help='Column number as primary key. (range: 1-N, default: 1)')
    parser.add_argument('-t', '--has-title', action='store_true', help='Treat the first line as a header.')
    parser.add_argument('--hide-index', action='store_true', help='Do not print row/column indexes.')
    parser.add_argument('--hide-keyname', action='store_true', help='Do not print row/column key names.')
    parser.add_argument('--hide-value', action='store_true', help='Do not print difference values.')
    args = parser.parse_args()
    # correct column number to start with 0
    args.primarykey -= 1

    # read csv
    csv1, header1 = read_csv(args.csv1, args.encoding, args.primarykey, args.has_title)
    csv2, header2 = read_csv(args.csv2, args.encoding, args.primarykey, args.has_title)
    # check column count
    if len(header1) != len(header2):
        print('error: different column count in CSV files.')
        return

    # get diff info
    diffs = diff_csv(csv1, header1, csv2, header2, args.primarykey)
    # print result
    print_diffs(diffs, args.hide_index, args.hide_keyname, args.hide_value)


def read_csv(fname: str, encoding: str, primarykey: int, has_header: bool):
    """Read csv and post-processing

    Args:
        fname (str): CSV file.
        encoding (str): encoding for CSV File.
        primarykey (int): colmn index of primary key.
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

    # Sort by primary key
    csvdata.sort(key=lambda x: x[primarykey])

    return csvdata, header


def diff_csv(csv1: list[list[str]], header1: list[str],
             csv2: list[list[str]], header2: list[str], primarykey: int):
    """Diff CSV files.

    Args:
        csv1 (list[list[str]]): 1st CSV data.
        header1 (list[str]): 1st CSV header.
        csv2 (list[list[str]]): 2nd CSV data.
        header2 (list[str]): 2nd CSV header.
        primarykey (int): colmn index of primary key.

    Returns:
        _type_: _description_
    """
    diffs = []

    ri1 = ri2 = 0
    while True:
        # get target row
        row1 = csv1[ri1] if len(csv1) > ri1 else None
        row2 = csv2[ri2] if len(csv2) > ri2 else None
        # get primary key of target row
        pkey1 = row1[primarykey] if row1 else None
        pkey2 = row2[primarykey] if row2 else None

        # exit when both CSV data is terminated
        if row1 is None and pkey2 is None:
            break

        # remaining lines of csv2, if csv1 is terminated
        # (== the row in csv2 only)
        elif pkey1 is None:
            diffs.append(DiffInfo(
                mark='+',
                index=f'R{str(ri2+1)}',
                keyname='',
                value=','.join(row2),
            ))
            ri2 += 1

        # remaining lines of csv1, if csv2 is terminated
        # (== the row in csv1 only)
        elif pkey2 is None:
            diffs.append(DiffInfo(
                mark='-',
                index=f'R{str(ri1+1)}',
                keyname='',
                value=','.join(row1),
            ))
            ri1 += 1

        # the row in csv2 only
        elif pkey1 > pkey2:
            diffs.append(DiffInfo(
                mark='+',
                index=f'R{str(ri2+1)}',
                keyname='',
                value=','.join(row2),
            ))
            ri2 += 1

        # the row in csv1 only
        elif pkey1 < pkey2:
            diffs.append(DiffInfo(
                mark='-',
                index=f'R{str(ri1+1)}',
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
                        index=f'R{ri1+1}|{ri2+1},C{ci+1}',
                        keyname=f'{pkey1} / {header1[ci]}',
                        value=f'"{v1}" <> "{v2}"',
                    ))
            ri1 += 1
            ri2 += 1

    return diffs


def print_diffs(diffs, hide_index, hide_keyname, hide_value):
    """Print diffs.

    Args:
        diffs (list[DiffInfo]): list of diff infos.
        hide_index (bool): if true then do not print indexes.
        hide_keyname (bool): if true then do not print key names.
        hide_value (bool): if true then do not print values.
    """

    for diff in diffs:
        pstr = f'{diff.mark} '
        if not hide_index and diff.index:
            pstr += f'{diff.index} '
        if not hide_keyname and diff.keyname:
            pstr += f'<{diff.keyname}> '
        if not hide_value and diff.value:
            pstr += f': {diff.value}'
        print(pstr)
    print(f'(diff count: {len(diffs)})')


if __name__ == '__main__':
    main()

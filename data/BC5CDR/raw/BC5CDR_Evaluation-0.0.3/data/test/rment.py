import sys
import json
from itertools import groupby
from turtle import title


inp_f = sys.argv[1]
out_f = sys.argv[2]


def read_pubtator(file):
    file = open(file, "r")
    lines = (line.strip() for line in file)
    for k, g in groupby(lines, key=bool):
        g = list(g)
        if g[0]:
            yield g
    file.close()

def extract_pubtator(lines):
    res = []
    fixed_lines = [
        str_with_null.replace('\x00', '')
        for str_with_null in lines[2:]
    ]
    for line in fixed_lines:
        sline = line.split('\t')
        if sline[1] == 'CID':
            res.append(line+'\t1.0')
    return res

data = read_pubtator(inp_f)
with open(out_f, 'w') as f:
    for sample in data:
        lines = extract_pubtator(sample)
        lines = '\n'.join(lines)
        print(lines[:-1], file=f)

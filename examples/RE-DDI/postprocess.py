# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import os
import sys
import re
import json


out_file = sys.argv[1]

prefix = [
    '(learned[0-9]+ )+',
    'we can conclude that',
    'we have that',
    'in conclusion,',
    ]


def strip_prefix(line):
    for p in prefix:
        res = re.search(p, line)
        if res is not None:
            line = re.split(p, line)[-1].strip()
            break
    return line


def split_sentence(line):
    sentences = re.split(r"; ", line)
    return sentences


def convert_relis_sentence(sentence):
    ans = None
    segs = re.match(r"the interaction between (.*) and (.*) is (.*)", sentence)
    if segs is not None:
        segs = segs.groups()
        ans = (segs[0].strip(), segs[2].strip(), segs[1].strip())
    return ans


def converter(sample, h_idx=0, r_idx=1, t_idx=2):
    ret = {"triple_list_gold": [], "triple_list_pred": [], "new": [], "lack": [], "id": [0]}
    for s in sample:
        ret["triple_list_pred"].append({"subject": s[h_idx], "relation": s[r_idx], "object": s[t_idx]})
    return ret


all_lines = []
with open(out_file, "r", encoding="utf8") as fr:
    for line in fr:
        e = line.strip()
        if len(e) > 0 and e[-1] == ".":
            all_lines.append(e[:-1])
        else:
            all_lines.append(e)


hypothesis = []
cnt = 0
fail_cnt = 0


for i, line in enumerate(all_lines):
    cnt += 1
    ret = []
    strip_line = strip_prefix(line)
    sentences = split_sentence(strip_line)
    for sen in sentences:
        ans = convert_relis_sentence(sen)
        if ans is not None:
            ret.append(ans)
    if len(ret) > 0:
        hypothesis.append(ret)
    else:
        hypothesis.append([("failed", "failed", "failed")])
        fail_cnt += 1
        print("Failed:id:{}, line:{}".format(i+1, line))


ret_formatted = []
for i in range(len(hypothesis)):
    ret_formatted.append(converter(hypothesis[i]))


with open(f"{out_file}.extracted.json", "w", encoding="utf8") as fw:
    for eg in ret_formatted:
        print(json.dumps(eg), file=fw)


print(f"failed = {fail_cnt}, total = {cnt}")

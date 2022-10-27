# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import os
import sys
import re
import json


out_file = sys.argv[1]
entity_file=sys.argv[2]
pmids_file = sys.argv[3]

prefix = [
    '(learned[0-9]+ )+',
    'in conclusion ,',
    'we can conclude that',
    'we have that',
    ]


def strip_prefix(line):
    for p in prefix:
        res = re.search(p, line)
        if res is not None:
            line = re.split(p, line)[-1].strip()
            break
    return line


def split_sentence(line):
    sentences = re.split(r";", line)
    return sentences


def convert_relis_sentence(sentence):
    ans = None
    segs = re.match(r"the relation between (.*) and (.*) exists", sentence.strip())
    if segs is not None:
        segs = segs.groups()
        chemical = segs[0].strip()
        disease = segs[1].strip()
        ans = (chemical, disease)
    return ans


all_lines = []
with open(out_file, "r", encoding="utf8") as fr:
    for line in fr:
        e = line.strip()
        if e[-1] == ".":
            all_lines.append(e[:-1])
        else:
            all_lines.append(e)
with open(entity_file, "r", encoding="utf8") as fr:
    ent2id = json.load(fr)
with open(pmids_file, "r") as reader:
    if '.json' in pmids_file:
        pmids = json.load(reader)
    else:
        pmids = []
        for line in reader:
            pmids.append(line.strip())


hypothesis = []
cnt = 0
fail_cnt = 0
for i, line in enumerate(all_lines):
    cnt += 1
    strip_line = strip_prefix(line)
    ret = []
    sentences = split_sentence(strip_line)
    for sen in sentences:
        ans = convert_relis_sentence(sen)
        if ans is not None:
            chemical, disease = ans
            chemicalID = ent2id['chemical2id'].get(chemical.strip(), "-1")
            diseaseID = ent2id['disease2id'].get(disease.strip(), "-1")
            ret.append(f"{pmids[i]}\tCID\t{chemicalID}\t{diseaseID}\t1.0")
    if len(ret) > 0:
        hypothesis.extend(ret)
    else:
        fail_cnt += 1
        print("Failed:id:{}, line:{}".format(i+1, line))


with open(f"{out_file}.extracted.PubTator", "w", encoding="utf8") as fw:
    for line in hypothesis:
        print(line, file=fw)


print(f"failed = {fail_cnt}, total = {cnt}")
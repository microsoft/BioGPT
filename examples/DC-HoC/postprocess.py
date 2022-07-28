import sys
import re


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


def convert_ansis_sentence(sentence):
    ans = None
    segs = re.search(r"the type of this document is(.*)", sentence)
    if segs is not None:
        segs = segs.groups()
        ans = segs[0].strip()
    return ans


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
    strip_line = strip_prefix(line)
    ans = convert_ansis_sentence(strip_line)
    if ans is not None:
        hypothesis.append(ans)
    else:
        hypothesis.append("failed")
        fail_cnt += 1
        print("Failed:id:{}, line:{}".format(i+1, line))


with open(f"{out_file}.extracted.txt", "w", encoding="utf8") as fw:
    for eg in hypothesis:
        print(eg, file=fw)


print(f"failed = {fail_cnt}, total = {cnt}")

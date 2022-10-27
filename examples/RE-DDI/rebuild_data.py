# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import os
import sys
import json

data_dir=sys.argv[1]


def sort_triples(triples, text):
    sorted_triples = sorted(triples, key=lambda x:text.find(x['drug']))
    return sorted_triples


def build_target_seq_relis(triples):        
    answer = ""
    for z in triples:
        drug = z["drug"].lower()
        target = z["target"].lower()
        rel = z["interaction"].lower()
        answer += f"the interaction between {drug} and {target} is {rel}; "

    return answer[:-2] + "."


def build_target_seq_2type(triples):        
    answer = ""
    for z in triples:
        drug = z["drug"].lower()
        target = z["target"].lower()
        rel = z["interaction"].lower()
        answer += f"{drug} and {target} are {rel}; "

    return answer[:-2] + "."


def loader(fname, fn):
    ret = []
    null_cnt = 0
    suc_cnt = 0
    null_flag = False
    with open(fname, "r", encoding="utf8") as fr:
        data = json.load(fr)
    for pmid, v in data.items():
        content = v["abstract"].strip().replace('\n',' ')

        content = content.lower()
        if v["triples"] is None or len(v["triples"]) == 0:
            if not null_flag:
                print(f"Following PMID in {fname} has no extracted triples:")
                null_flag = True
            print(f"{pmid} ", end="")
            null_cnt += 1
        else:
            triples = v['triples']
            triples = sort_triples(triples, content)
            answer = fn(triples)
            ret.append((pmid, content, answer))
            suc_cnt += 1
    if null_flag:
        print("")
    print(f"{len(data)} samples in {fname} has been processed with {null_cnt} samples has no triples extracted.")
    return ret


def dumper(content_list, prefix):
    fw_pmid = open(prefix + ".pmid", "w")
    fw_content = open(prefix + ".x", "w")
    fw_label = open(prefix + ".y", "w")
    
    for pmid, x, y in content_list:
        print(pmid, file=fw_pmid)
        print(x, file=fw_content)
        print(y, file=fw_label)

    fw_pmid.close()
    fw_content.close()
    fw_label.close()


def worker(fname, prefix, fn):
    ret = loader(fname, fn)
    dumper(ret, prefix)
           

for split in ['train', 'valid', 'test']:
    worker(os.path.join(f"{data_dir}", f"{split}.json"), os.path.join(f"{data_dir}", f"relis_{split}"), build_target_seq_relis)

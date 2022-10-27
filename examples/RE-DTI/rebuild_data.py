# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import os
import sys
import json
import re

data_dir=sys.argv[1]

def map_relation_to_verb(relation):
    special_mapping = {
        "product of": "is the product of",
        "negative modulator": "negatively modulates",
        "other/unknown": "randomly works with",
        "other": "randomly works with",
        "incorporation into and destabilization": "incorporates into and destabilizates",
        "cross-linking/alkylation": "cross lines / alkylates",
        "antibody": "is the antibody of",
        "downregulator": "downregulates",
        "desensitize the target": "desensitizes",
        "protector": "protects",
        "inhibitor": "inhibits",
        "weak inhibitor": "weakly inhibits",
        "blocker": "blocks"
    }
    if relation in special_mapping:
        return special_mapping[relation]

    if relation.endswith("agonist") or relation.endswith("antagonist"):
        return relation + "s"
    
    if relation.endswith("or") or relation.endswith("er"):
        return relation[:-2] + "es"

    if relation.endswith("tion"):
        return relation[:-3] + "es"

    if relation.endswith("ing"):
        return relation[:-3] + "s"

    return relation + "s"


def sort_triples(triples, text):
    sorted_triples = sorted(triples, key=lambda x:text.find(x['drug']))
    return sorted_triples


def build_target_seq_svo(triples):        
    answer = ""
    for z in triples:
        drug = z["drug"].lower()
        target = z["target"].lower()
        rel = map_relation_to_verb(z["interaction"].lower())
        answer += f"{drug} {rel} {target}; "

    return answer[:-2] + "."


def build_target_seq_isof(triples):        
    answer = ""
    for z in triples:
        drug = z["drug"].lower()
        target = z["target"].lower()
        rel = z["interaction"].lower()
        answer += f"{drug} is the {rel} of {target}; "

    return answer[:-2] + "."


def build_target_seq_htr(triples):        
    answer = ""
    for z in triples:
        drug = z["drug"].lower()
        target = z["target"].lower()
        rel = z["interaction"].lower()
        answer += f"<h> {drug} <t> {target} <r> {rel} "

    return answer[:-1] + "."


def build_target_seq_relis(triples):        
    answer = ""
    for z in triples:
        drug = z["drug"].lower()
        target = z["target"].lower()
        rel = z["interaction"].lower()
        answer += f"the interaction between {drug} and {target} is {rel}; "

    return answer[:-2] + "."


def loader(fname, fn):
    ret = []
    null_cnt = 0
    suc_cnt = 0
    null_flag = False
    with open(fname, "r", encoding="utf8") as fr:
        data = json.load(fr)
    for pmid, v in data.items():
        if re.search(r"\W$", v["title"]):
            content = v["title"] + " " + v["abstract"]
        else:
            content = v["title"] + ". " + v["abstract"]

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
    
    for ele in content_list:
        print(ele[0], file=fw_pmid)
        print(ele[1], file=fw_content)
        print(ele[2], file=fw_label)

    fw_pmid.close()
    fw_content.close()
    fw_label.close()


def worker(fname, prefix, fn):
    ret = loader(fname, fn)
    dumper(ret, prefix)
           

for split in ['train', 'valid', 'test']:
    worker(os.path.join(f"{data_dir}", f"{split}.json"), os.path.join(f"{data_dir}", f"relis_{split}"), build_target_seq_relis)
    #worker(os.path.join(f"{data_dir}", f"{split}.json"), os.path.join(f"{data_dir}", f"isof_{split}"), build_target_seq_isof)
    #worker(os.path.join(f"{data_dir}", f"{split}.json"), os.path.join(f"{data_dir}", f"svo_{split}"), build_target_seq_svo)
    #worker(os.path.join(f"{data_dir}", f"{split}.json"), os.path.join(f"{data_dir}", f"htr_{split}"), build_target_seq_htr)
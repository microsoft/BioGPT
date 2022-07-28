import os
import sys
import json
import re

data_dir=sys.argv[1]


def unify_ent2id(ent2id, method='max'):
    id2ent = {}
    for k, v in ent2id.items():
        if v in id2ent:
            if method == 'min':
                id2ent[v] = k if len(k) < len(id2ent[v]) else id2ent[v]
            else:
                id2ent[v] = k if len(k) > len(id2ent[v]) else id2ent[v]
        else:
            id2ent[v] = k
    ent2id = {v:k for k, v in id2ent.items()}
    return ent2id, id2ent
    

def sort_triples(triples, text):
    sorted_triples = sorted(triples, key=lambda x:text.find(x['chemical']))
    return sorted_triples


def build_target_seq_svo(relations, id2chem, id2disease):        
    answer = ""
    for z in relations:
        chemical = id2chem[z["chemical"]]
        disease = id2disease[z["disease"]]
        answer += f"{chemical} correlates with {disease}; "
    return answer[:-2] + "."


def build_target_seq_relis(relations, id2chem, id2disease):        
    answer = ""
    for z in relations:
        chemical = id2chem[z["chemical"]]
        disease = id2disease[z["disease"]]
        answer += f"the relation between {chemical} and {disease} exists; "
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
        
        if v["relations"] is None or len(v["relations"]) == 0:
            if not null_flag:
                print(f"Following PMID in {fname} has no extracted relations:")
                null_flag = True
            print(f"{pmid} ", end="")
            null_cnt += 1
        else:
            chemical2id = v["chemical2id"]
            disease2id = v["disease2id"]
            unified_chemical2id, id2chemical = unify_ent2id(chemical2id, method='max')
            unified_disease2id, id2disease = unify_ent2id(disease2id, method='max')
            answer = fn(v["relations"], id2chemical, id2disease)
            ret.append((pmid, content, answer))
            suc_cnt += 1
    if null_flag:
        print("")
    print(f"{len(data)} samples in {fname} has been processed with {null_cnt} samples has no relations extracted.")
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
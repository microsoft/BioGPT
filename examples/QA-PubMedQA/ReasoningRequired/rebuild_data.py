# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import os
import sys
import re
import json

data_dir=sys.argv[1]
prefix=sys.argv[2]


def build_source_seq(question, context, long_answer=None):
    if long_answer:
        src = "question: {} context: {} answer: {}".format(question.strip(), context.strip(), long_answer.strip())
    else:
        src = "question: {} context: {} ".format(question.strip(), context.strip())
    return src


def build_target_seq(tgt):
    tgt = 'the answer to the question given the context is ' + tgt + '.'
    return tgt


def loader(fname, fn, required_long_answer=False):
    ret = []
    cnt = 0
    
    with open(fname, 'r') as file:
        data = json.load(file)
    
    for pmid, content in data.items():
        cnt += 1
        question = content['QUESTION']
        context = ' '.join(sen.strip() for sen in content['CONTEXTS'])
        context = re.sub(r'\n', ' ', context)
        # remove duplicate spaces
        context = re.sub(r'\s+', ' ', context)
        long_answer = content['LONG_ANSWER']
        if required_long_answer:
            source = build_source_seq(question, context, long_answer)
        else:
            source = build_source_seq(question, context)

        if 'final_decision' in content:
            label = content['final_decision']
            target = fn(label)
        else:
            target = ''
        if isinstance(target, list):
            for i in range(len(target)):
                data_pair = [source, target[i]]
                ret.append(data_pair)
        else:
            data_pair = [source, target]
            ret.append(data_pair)

    print(f"{cnt} samples in {fname} has been processed")
    return ret


def dumper(content_list, prefix):
    fw_source = open(prefix + ".x", "w")
    fw_target = open(prefix + ".y", "w")
    
    for ele in content_list:
        print(ele[0], file=fw_source)
        print(ele[1], file=fw_target)

    fw_source.close()
    fw_target.close()


def worker(fname, prefix, fn):
    ret = loader(fname, fn)
    dumper(ret, prefix)


worker(os.path.join(f"{data_dir}", "pqal_train_set.json"), os.path.join(f"{data_dir}", f"{prefix}_train"), build_target_seq)
worker(os.path.join(f"{data_dir}", "pqal_dev_set.json"), os.path.join(f"{data_dir}", f"{prefix}_valid"), build_target_seq)
worker(os.path.join(f"{data_dir}", "pqal_test_set.json"), os.path.join(f"{data_dir}", f"{prefix}_test"), build_target_seq)
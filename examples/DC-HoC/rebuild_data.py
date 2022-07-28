import os
import sys

data_dir=sys.argv[1]


def build_target_seq(tgt):
    tgt = 'the type of this document is ' + tgt + '.'
    return tgt


def loader(fname, fn):
    ret = []
    cnt = 0
    file = open(fname)
    
    for line in file:
        
        if line == '\n':
            continue
        cnt += 1
        sent = line.split('\t')
        source, target = sent[0].replace('\n', '').strip(), sent[1].replace('\n', '').strip()
        if source[-1] == '.':
            ret.append([source, fn(target)])
        else:
            ret.append([source +'.', fn(target)])

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


for split in ['train', 'valid', 'test']:
    worker(os.path.join(f"{data_dir}", f"{split}.tsv"), os.path.join(f"{data_dir}", f"ansis_{split}"), build_target_seq)
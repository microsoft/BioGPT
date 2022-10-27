# coding: utf-8
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from ast import Global
import os
import sys
from sklearn.metrics import f1_score
from sklearn.preprocessing import MultiLabelBinarizer

pred_file = sys.argv[1]
gold_file = sys.argv[2]


def convert_hoc_labels(lines):
    labels = []
    classes = ['tumor promoting inflammation', 'inducing angiogenesis', 'evading growth suppressors', 'resisting cell death', 'cellular energetics', 'empty', 'genomic instability and mutation', 'sustaining proliferative signaling', 'avoiding immune destruction', 'activating invasion and metastasis', 'enabling replicative immortality']
    for line in lines:
        labels.append([w.strip() for w in line.strip().split('|')])
    return MultiLabelBinarizer(classes=classes).fit_transform(labels)

def do_eval(preds, golden):
    preds = convert_hoc_labels(preds)
    golden = convert_hoc_labels(golden)
    score = f1_score(golden, preds, average='micro')
    print(score)
    return


def main():
    preds = []
    with open(pred_file) as reader:
        for line in reader:
            preds.append(line.strip())

    golden = []
    with open(gold_file) as reader:
        for line in reader:
            line = line.strip()
            if line != '' and len(line) > 0:
                golden.append(line.strip().split('\t')[-1])
    
    assert len(preds) == len(golden), f"{len(preds)} {len(golden)}"

    print("\n====File: ", os.path.basename(pred_file))
    do_eval(preds, golden)


if __name__ == "__main__":
    main()

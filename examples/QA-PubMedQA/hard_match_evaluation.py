# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import os
import sys
import json
from sklearn.metrics import accuracy_score

pred_file = sys.argv[1]
gold_file = sys.argv[2]


def do_eval(preds, golden):
    print(accuracy_score(golden, preds))
    return


def main():
    preds = []
    with open(pred_file) as reader:
        for line in reader:
            preds.append(line.strip())

    golden = []
    if gold_file.endswith('.tsv'):
        with open(gold_file) as reader:
            for line in reader:
                line = line.strip()
                if line != '' and len(line) > 0:
                    golden.append(line.strip().split('\t')[-1])
    elif gold_file.endswith('.json'):
        with open(gold_file) as reader:
            data = json.load(reader)
            golden = [label for pmid, label in data.items()]
    assert len(preds) == len(golden), f"{len(preds)} {len(golden)}"

    print("\n====File: ", os.path.basename(pred_file))
    do_eval(preds, golden)


if __name__ == "__main__":
    main()

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import os
import sys
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

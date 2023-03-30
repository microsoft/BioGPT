# Question Answering on PubMedQA in Reasoning Required Setting

## Data
Download data from [PubMedQA](https://github.com/pubmedqa/pubmedqa) and following the steps of splitting dataset.

Copy the files `pqal_fold0/train_set.json`, `pqal_fold0/dev_set.json`, `test_set.json` and `test_ground_truth.json` to `../../../data/PubMedQA/raw` and rename them:

``` bash
mv train_set.json pqal_train_set.json
mv dev_set.json pqal_dev_set.json
mv test_set.json pqal_test_set.json
```

Then, you can process the data by:
``` bash
bash preprocess.sh # for BioGPT
```
or:
``` bash
bash preprocess_large.sh # for BioGPT-Large
```

## Model Checkpoint
We provide our fine-tuned model on the task. See [here](../../../README.md#pre-trained-models)

## Inference and Evaluating
You can inference and evaluate the model on the test set by:
``` bash
bash infer.sh # for BioGPT
```
or 
``` bash
bash infer_large.sh # for BioGPT-Large
```
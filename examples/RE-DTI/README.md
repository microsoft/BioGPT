# Relation Extraction on KD-DTI

## Data
According to the original [KD-DTI dataset](https://github.com/bert-nmt/BERT-DTI), before processing the data, you should first register a DrugBank account, download the xml dataset and replace the entity id with the entity name in the drugbank.

Then, you can process the data by:
``` bash
bash preprocess.sh
```

For more details, please see [here](https://github.com/bert-nmt/BERT-DTI).

## Training
You can fine-tune the pre-trained BioGPT on the task by:
``` bash
bash train.sh
```

## Model Checkpoint
We provide our fine-tuned model on the task. See [here](../../README.md#pre-trained-models)

## Inference and Evaluating
You can inference and evalaute the model on the test set by:
``` bash
bash infer.sh
```
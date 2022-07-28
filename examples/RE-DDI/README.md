# Relation Extraction on DDI

## Data
We assume you have downloaded all the data required and skip this step.
Otherwise, you can process the data yourself:
``` bash
bash preprocess.sh
```

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
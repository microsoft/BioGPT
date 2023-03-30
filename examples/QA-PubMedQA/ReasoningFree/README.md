# Question Answering on PubMedQA in Reasoning Free Setting

## Data
Download data from https://github.com/pubmedqa/pubmedqa
Following the steps of splitting data 
You can process the data by:
``` bash
bash preprocess.sh # for BioGPT
```
or:
``` bash
bash preprocess_large.sh # for BioGPT-Large
```

## Training
You can fine-tune on the pre-trained models by:
``` bash
bash train.sh # for BioGPT
```
or 
``` bash
bash train_large.sh # for BioGPT-Large
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
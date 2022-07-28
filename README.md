<p align="center">
  <a href="https://github.com/renqianluo/BioGPT/blob/master/LICENSE"><img alt="MIT License" src="https://img.shields.io/badge/license-MIT-blue.svg" /></a>
</p>

--------------------------------------------------------------------------------

# BioGPT
This repository contains the implementation of [BioGPT: Generative Pre-trained Transformer for Biomedical Text Generation and Mining](), by Renqian Luo, Liai Sun, Yingce Xia, Tao Qin and Tie-Yan Liu.


# Requirements and Installation

* [PyTorch](http://pytorch.org/) version >= 1.8.0
* Python version >= 3.7
* fairseq:

``` bash
git clone https://github.com/pytorch/fairseq
cd fairseq
git checkout dd7499
pip install .
```
* Moses
``` bash
git clone https://github.com/moses-smt/mosesdecoder.git
export MOSES=${PWD}/mosesdecoder
```
* fastBPE
``` bash
pip install fastBPE
git clone https://github.com/glample/fastBPE.git
export FASTBPE=${PWD}/fastBPE
cd fastBPE
g++ -std=c++11 -pthread -O3 fastBPE/main.cc -IfastBPE -o fast
```
* sacremoses
``` bash
pip install sacremoses
```
* sklearn
``` bash
pip install sklearn
```

Remember to set the environment variables `MOSES` and `FASTBPE` to the path of Moses and fastBPE respetively, as they will be required later.

# Getting Started
## Data preparation
You can download all the data we processed for downstream tasks [here](https://msralaphilly2.blob.core.windows.net/ml-la/release/BioGPT/data.tgz) and extract it to the root of this project, or you can process the data by yourself in the corresponding experiment.
``` bash
wget https://msralaphilly2.blob.core.windows.net/ml-la/release/BioGPT/data.tgz
tar -zxvf data.tgz
```
## Pre-trained models
We provide our pre-trained BioGPT model checkpoint along with fine-tuned checkpoints for downstream tasks [here](https://msralaphilly2.blob.core.windows.net/ml-la/release/BioGPT/checkpoints.tgz). Download it and extract it the root of this project.
``` bash
wget https://msralaphilly2.blob.core.windows.net/ml-la/release/BioGPT/checkpoints.tgz
tar -zxvf checkpoints.tgz
```

It contains following folders:

* Pre-trained-BioGPT: The pre-trained BioGPT model checkpoint
* RE-BC5CDR-BioGPT: The fine-tuned checkpoint for relation extraction task on BC5CDR
* RE-DTI-BioGPT: The fine-tuned checkpoint for relation extraction task on KD-DTI
* RE-DDI-BioGPT: The fine-tuned checkpoint for relation extraction task on DDI
* DC-HoC-BioGPT: The fine-tuned checkpoint for document classification task on HoC
* QA-PubMedQA-BioGPT: The fine-tuned checkpoint for question answering task on PubMedQA

## Example Usage
Use pre-trained BioGPT model in your code:
```python
import torch
from fairseq.models.transformer_lm import TransformerLanguageModel
m = TransformerLanguageModel.from_pretrained(
        "checkpoints/Pre-trained-BioGPT", 
        "checkpoint.pt", 
        "data/PubMed/data-bin",
        tokenizer='moses', 
        bpe='fastbpe', 
        bpe_codes="data/bpecodes",
        min_len=100,
        max_len_b=1024)
m.cuda()
src_tokens = m.encode("COVID-19 is")
generate = m.generate([src_tokens], beam=)[0]
output = m.decode(generate[0]["tokens"])
print(output)
```

Use fine-tuned BioGPT model on KD-DTI for drug-target-interaction in your code:
```python
import torch
from fairseq.models.transformer_lm import TransformerLanguageModel
m = TransformerLanguageModel.from_pretrained(
        "checkpoints/RE-DTI-BioGPT", 
        "checkpoint_avg.pt", 
        "data/KD-DTI/relis-bin",
        tokenizer='moses', 
        bpe='fastbpe', 
        bpe_codes="data/bpecodes",
        max_len_b=1024,
        beam=1)
m.cuda()
src_text="" # input text, e.g., a PubMed abstract
src_tokens = m.encode(src_text)
generate = m.generate([src_tokens], beam=args.beam)[0]
output = m.decode(generate[0]["tokens"])
print(output)
```

For more downstream tasks, please see below.

## Downstream tasks
See corresponding folder in [examples](examples):
### [Relation Extraction on BC5CDR](examples/RE-BC5CDR)
### [Relation Extraction on KD-DTI](examples/RE-DTI/)
### [Relation Extraction on DDI](examples/RE-DDI)
### [Document Classification on HoC](examples/DC-HoC/)
### [Question Answering on PubMedQA](examples/QA-PubMedQA/)
### [Text Generation](examples/text-generation/)

# License

BioGPT is MIT-licensed.
The license applies to the pre-trained models as well.

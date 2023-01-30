# BioGPT
This repository contains the implementation of [BioGPT: Generative Pre-trained Transformer for Biomedical Text Generation and Mining](https://academic.oup.com/bib/advance-article/doi/10.1093/bib/bbac409/6713511?guestAccessKey=a66d9b5d-4f83-4017-bb52-405815c907b9), by Renqian Luo, Liai Sun, Yingce Xia, Tao Qin, Sheng Zhang, Hoifung Poon and Tie-Yan Liu.

# News!
* BioGPT-Large model with 1.5B parameters is coming, currently available on PubMedQA task with SOTA performance of 81% accuracy. See [Question Answering on PubMedQA](examples/QA-PubMedQA/) for evaluation.


# Requirements and Installation

* [PyTorch](http://pytorch.org/) version == 1.12.0
* Python version == 3.10
* fairseq version == 0.12.0:

``` bash
git clone https://github.com/pytorch/fairseq
cd fairseq
git checkout v0.12.0
pip install .
python setup.py build_ext --inplace
cd ..
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
pip install scikit-learn
```

Remember to set the environment variables `MOSES` and `FASTBPE` to the path of Moses and fastBPE respetively, as they will be required later.

# Getting Started
## Pre-trained models
We provide our pre-trained BioGPT model checkpoint along with fine-tuned checkpoints for downstream tasks 

|Model|Description|URL|
|----|----|---|
|BioGPT|Pre-trained BioGPT model checkpoint|[link](https://msramllasc.blob.core.windows.net/modelrelease/BioGPT/checkpoints/Pre-trained-BioGPT.tgz)|
|BioGPT-QA-PubMedQA-BioGPT|Fine-tuned BioGPT for question answering task on PubMedQA|[link](https://msramllasc.blob.core.windows.net/modelrelease/BioGPT/checkpoints/QA-PubMedQA-BioGPT/)|
|BioGPT-QA-PubMEDQA-BioGPT-Large|Fine-tuned BioGPT-Large for question answering task on PubMedQA|[link](https://msramllasc.blob.core.windows.net/modelrelease/BioGPT/checkpoints/QA-PubMedQA-BioGPT-Large/)|
|BioGPT-RE-BC5CDR|Fine-tuned BioGPT for relation extraction task on BC5CDR|[link](https://msramllasc.blob.core.windows.net/modelrelease/BioGPT/checkpoints/RE-BC5CDR-BioGPT/)|
|BioGPT-RE-DDI|Fine-tuned BioGPT for relation extraction task on DDI|[link](https://msramllasc.blob.core.windows.net/modelrelease/BioGPT/checkpoints/RE-DDI-BioGPT/)|
|BioGPT-RE-DTI|Fine-tuned BioGPT for relation extraction task on KD-DTI|[link](https://msramllasc.blob.core.windows.net/modelrelease/BioGPT/checkpoints/RE-DTI-BioGPT/)|
|BioGPT-DC-HoC|Fine-tuned BioGPT for document classification task on HoC|[link](https://msramllasc.blob.core.windows.net/modelrelease/BioGPT/checkpoints/DC-HoC-BioGPT/)|

Download them and extract them to the `checkpoints` folder of this project.

For example:
``` bash
mkdir checkpoints
cd checkpoints
wget https://msramllasc.blob.core.windows.net/modelrelease/BioGPT/checkpoints/Pre-trained-BioGPT.tgz
tar -zxvf Pre-trained-BioGPT.tgz
```

## Example Usage
Use pre-trained BioGPT model in your code:
```python
import torch
from fairseq.models.transformer_lm import TransformerLanguageModel
m = TransformerLanguageModel.from_pretrained(
        "checkpoints/Pre-trained-BioGPT", 
        "checkpoint.pt", 
        "data",
        tokenizer='moses', 
        bpe='fastbpe', 
        bpe_codes="data/bpecodes",
        min_len=100,
        max_len_b=1024)
m.cuda()
src_tokens = m.encode("COVID-19 is")
generate = m.generate([src_tokens], beam=5)[0]
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

# Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

# Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft 
trademarks or logos is subject to and must follow 
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.

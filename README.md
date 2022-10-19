# BioGPT
This repository contains the implementation of [BioGPT: Generative Pre-trained Transformer for Biomedical Text Generation and Mining](https://academic.oup.com/bib/advance-article/doi/10.1093/bib/bbac409/6713511?guestAccessKey=a66d9b5d-4f83-4017-bb52-405815c907b9), by Renqian Luo, Liai Sun, Yingce Xia, Tao Qin, Sheng Zhang, Hoifung Poon and Tie-Yan Liu.


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
## Pre-trained models
We provide our pre-trained BioGPT model checkpoint along with fine-tuned checkpoints for downstream tasks [here](https://msralaphilly2.blob.core.windows.net/ml-la/release/BioGPT/checkpoints.tgz). Download it and extract it the root of this project. 
``` bash
wget https://msralaphilly2.blob.core.windows.net/ml-la/release/BioGPT/checkpoints.tgz
tar -zxvf checkpoints.tgz
```

### Note: 
If you encounter connection issue during downloading, it may be caused by the large model file size (22GB). We splitted the large files into pieces with each being 1GB. You can donwload them and use `cat` to concatenate them together: [part0](https://msralaphilly2.blob.core.windows.net/ml-la/release/BioGPT/checkpoints.tgz.00), [part1](https://msralaphilly2.blob.core.windows.net/ml-la/release/BioGPT/checkpoints.tgz.01), [part2](https://msralaphilly2.blob.core.windows.net/ml-la/release/BioGPT/checkpoints.tgz.02), [part3](https://msralaphilly2.blob.core.windows.net/ml-la/release/BioGPT/checkpoints.tgz.03), [part4](https://msralaphilly2.blob.core.windows.net/ml-la/release/BioGPT/checkpoints.tgz.04), [part5](https://msralaphilly2.blob.core.windows.net/ml-la/release/BioGPT/checkpoints.tgz.05), [part6](https://msralaphilly2.blob.core.windows.net/ml-la/release/BioGPT/checkpoints.tgz.06), [part7](https://msralaphilly2.blob.core.windows.net/ml-la/release/BioGPT/checkpoints.tgz.07), [part8](https://msralaphilly2.blob.core.windows.net/ml-la/release/BioGPT/checkpoints.tgz.08), [part9](https://msralaphilly2.blob.core.windows.net/ml-la/release/BioGPT/checkpoints.tgz.09), [part10](https://msralaphilly2.blob.core.windows.net/ml-la/release/BioGPT/checkpoints.tgz.10), [part11](https://msralaphilly2.blob.core.windows.net/ml-la/release/BioGPT/checkpoints.tgz.11), [part12](https://msralaphilly2.blob.core.windows.net/ml-la/release/BioGPT/checkpoints.tgz.12), [part13](https://msralaphilly2.blob.core.windows.net/ml-la/release/BioGPT/checkpoints.tgz.13), [part14](https://msralaphilly2.blob.core.windows.net/ml-la/release/BioGPT/checkpoints.tgz.14), [part15](https://msralaphilly2.blob.core.windows.net/ml-la/release/BioGPT/checkpoints.tgz.15), [part16](https://msralaphilly2.blob.core.windows.net/ml-la/release/BioGPT/checkpoints.tgz.16), [part17](https://msralaphilly2.blob.core.windows.net/ml-la/release/BioGPT/checkpoints.tgz.17), [part18](https://msralaphilly2.blob.core.windows.net/ml-la/release/BioGPT/checkpoints.tgz.18), [part19](https://msralaphilly2.blob.core.windows.net/ml-la/release/BioGPT/checkpoints.tgz.19), [part20](https://msralaphilly2.blob.core.windows.net/ml-la/release/BioGPT/checkpoints.tgz.20), [part21](https://msralaphilly2.blob.core.windows.net/ml-la/release/BioGPT/checkpoints.tgz.21)
``` bash
# download all the splitted files from above.
for i in `seq 0 21`; do wget `printf "https://msralaphilly2.blob.core.windows.net/ml-la/release/BioGPT/checkpoints.tgz.%02d" $i`; done
# cat them together and decompress
cat checkpoints.tgz.* | tar -zxvf -
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

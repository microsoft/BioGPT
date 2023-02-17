from fairseq.models.transformer_lm import TransformerLanguageModel
from src.transformer_lm_prompt import TransformerLanguageModelPrompt

from server.utils import singleton


class DefaultModel:
    @classmethod
    def clean_output(cls, output):
        return output.split("learned9")[-1]


@singleton
class PretrainedBioGPT(DefaultModel):
    def __init__(self):
        self.m = TransformerLanguageModel.from_pretrained(
            "checkpoints/Pre-trained-BioGPT",
            "checkpoint.pt",
            "data",
            tokenizer='moses',
            bpe='fastbpe',
            bpe_codes="data/bpecodes",
            min_len=100,
            max_len_b=1024
        )

    @classmethod
    def clean_output(cls, output):
        return output


@singleton
class PretrainedBioGPTLarge(DefaultModel):
    def __init__(self):
        self.m = TransformerLanguageModel.from_pretrained(
            "checkpoints/Pre-trained-BioGPT-Large",
            "checkpoint.pt",
            "data/BioGPT-Large",  # change this for smaller model
            tokenizer='moses',
            bpe='fastbpe',
            bpe_codes="data/BioGPT-Large/bpecodes",
            min_len=100
        )

    @classmethod
    def clean_output(cls, output):
        return output


@singleton
class Pubmed(DefaultModel):
    def __init__(self):
        self.m = TransformerLanguageModelPrompt.from_pretrained(
            "checkpoints/QA-PubMedQA-BioGPT",
            "checkpoint_avg.pt",
            "data/PubMedQA/ansis-bin",
            tokenizer='moses',
            bpe='fastbpe',
            bpe_codes="data/bpecodes",
            min_len=100,
            max_len_b=1024
        )


@singleton
class PubmedLarge(DefaultModel):
    def __init__(self):
        self.m = TransformerLanguageModelPrompt.from_pretrained(
            "checkpoints/QA-PubMedQA-BioGPT-Large",
            "checkpoint_avg.pt",
            "data/PubMedQA/biogpt-large-ansis-bin",
            tokenizer='moses',
            bpe='fastbpe',
            bpe_codes="data/BioGPT-Large/bpecodes",
            min_len=100,
            max_len_b=1024,
            beam=1
        )


@singleton
class DTI(DefaultModel):
    def __init__(self):
        self.m = TransformerLanguageModelPrompt.from_pretrained(
            "checkpoints/RE-DTI-BioGPT",
            "checkpoint_avg.pt",
            "data/KD-DTI/relis-bin",
            tokenizer='moses',
            bpe='fastbpe',
            bpe_codes="data/bpecodes",
            max_len_b=1024,
            beam=1
        )


@singleton
class DDI(DefaultModel):
    def __init__(self):
        self.m = TransformerLanguageModelPrompt.from_pretrained(
            "checkpoints/RE-DDI-BioGPT",
            "checkpoint_avg.pt",
            "data/DDI/relis-bin",
            tokenizer='moses',
            bpe='fastbpe',
            bpe_codes="data/bpecodes",
            max_len_b=1024,
            beam=1
        )


@singleton
class BC5CDR(DefaultModel):
    def __init__(self):
        self.m = TransformerLanguageModelPrompt.from_pretrained(
            "checkpoints/RE-BC5CDR-BioGPT",
            "checkpoint_avg.pt",
            "data/BC5CDR/relis-bin",
            tokenizer='moses',
            bpe='fastbpe',
            bpe_codes="data/bpecodes",
            max_len_b=1024,
            beam=1
        )


@singleton
class DocumentClassification(DefaultModel):
    def __init__(self):
        self.m = TransformerLanguageModelPrompt.from_pretrained(
            "checkpoints/DC-HoC-BioGPT",
            "checkpoint_last.pt",
            "data/HoC/ansis-bin",
            tokenizer='moses',
            bpe='fastbpe',
            bpe_codes="data/bpecodes",
            min_len=100,
            max_len_b=1024
        )

    @classmethod
    def clean_output(cls, output):
        split_output = output.split("learned1")[1:]
        return " ".join(split_output)

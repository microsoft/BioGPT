from fairseq.models.transformer_lm import TransformerLanguageModel

from server.utils import singleton


@singleton
class Models:

    def __init__(self):
        self.trained_biogpt = TransformerLanguageModel.from_pretrained(
            "checkpoints/Pre-trained-BioGPT",
            "checkpoint.pt",
            "data",
            tokenizer='moses',
            bpe='fastbpe',
            bpe_codes="data/bpecodes",
            min_len=100,
            max_len_b=1024
        )

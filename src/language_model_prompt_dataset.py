import logging

import numpy as np
import torch
from fairseq.data import FairseqDataset, data_utils


logger = logging.getLogger(__name__)


def collate(samples, pad_idx, eos_idx, prefix=False, sep_idx=None, prompt=None):
    if len(samples) == 0:
        return {}

    def make_sentence(prompt, source, target):
        if source[-1] == eos_idx:
            source = source[:-1]
        if prompt is None:
            return torch.cat([source, target], dim=0)
        if prefix:
            sep = torch.LongTensor([sep_idx])
            return torch.cat([prompt, source, sep, target], dim=0)
        return torch.cat([source, prompt, target], dim=0)
        
            
    def merge(tokens, move_eos_to_beginning=False):
        return data_utils.collate_tokens(
            tokens,
            pad_idx,
            eos_idx,
            move_eos_to_beginning=move_eos_to_beginning,
        )

    id = torch.LongTensor([s["id"] for s in samples])
    #src_tokens = merge([s["source"] for s in samples])
    #src_lengths = torch.LongTensor([s["source"].ne(pad_idx).long().sum() for s in samples])

    target_tokens = []
    target_lengths = []
    for s in samples:
        target_tokens.append(make_sentence(prompt, s["source"], s["target"]))
        
    target_lengths = [t.ne(pad_idx).long().sum() for t in target_tokens]
    target = merge(target_tokens)
    target_lengths = torch.LongTensor(target_lengths)
    prev_output_tokens = merge(target_tokens, move_eos_to_beginning=True)
    ntokens = target_lengths.sum().item()
    batch = {
        "id": id,
        "nsentences": len(samples),
        "ntokens": ntokens,
        "net_input": {
            "src_tokens": prev_output_tokens, #src_tokens,
            "src_lengths": target_lengths, #src_lengths,
            #"prev_output_tokens": prev_output_tokens,
            #"target_lengths": target_lengths,
        },
        "target": target,
    }
    return batch


class LanguageModelPromptDataset(FairseqDataset):
    """
    A pair of torch.utils.data.Datasets.

    Args:
        src (torch.utils.data.Dataset): source dataset to wrap
        src_sizes (List[int]): source sentence lengths
        dictionary (~fairseq.data.Dictionary): vocabulary
        tgt (torch.utils.data.Dataset, optional): target dataset to wrap
        tgt_sizes (List[int], optional): target sentence lengths
        prefix (bool, optional): prefix
        prompt (str, optional): prompt to use
        shuffle (bool, optional): shuffle dataset elements before batching
            (default: True).
        max_source_length (int): max source text length
        max_length (int): max text length
        prompt_length (int): length of the prompt text
        
    """

    def __init__(
        self,
        src,
        src_sizes,
        dictionary,
        tgt,
        tgt_sizes,
        prefix=False,
        prompt=None,
        shuffle=True,
        eos=None,
        max_source_length=None,
        max_length=None,
        prompt_length=None,
    ):
        self.src = src
        self.tgt = tgt
        self.prefix = prefix
        self.seq_sep = None
        self.prompt = prompt
        self.dict = dictionary
        self.shuffle = shuffle
        self.eos = eos if eos is not None else dictionary.eos()
        self.max_source_length = max_source_length
        self.max_target_length = max_length - max_source_length - prompt_length
        if self.prefix:
            self.max_target_length -= 1
        self.src_sizes = [min(s-1, self.max_source_length) for s in src_sizes]
        self.tgt_sizes = [min(t, self.max_target_length) for t in tgt_sizes]
        self.sizes = np.array([s+t for s,t in zip(self.src_sizes, self.tgt_sizes)])
        self.buckets = None
        
    def get_batch_shapes(self):
        return self.buckets

    def __getitem__(self, index):
        src_item = self.src[index]
        if src_item.size(0) - 1 > self.max_source_length:
            src_item = src_item[:self.max_source_length + 1]
            src_item[-2] = self.dict.index('...')
            src_item[-1] = self.eos
        
        tgt_item = self.tgt[index]
        if tgt_item.size(0) > self.max_target_length:
            tgt_item = tgt_item[:self.max_target_length]
            tgt_item[-2] = self.dict.index('...')
            tgt_item[-1] = self.eos
        example = {
            "id": index,
            "source": src_item,
            "target": tgt_item,
        }
        return example

    def __len__(self):
        return len(self.src)

    def collater(self, samples):
        """Merge a list of samples to form a mini-batch.

        Args:
            samples (List[dict]): samples to collate
        Returns:
            dict: a mini-batch with the following keys:

                - `id` (LongTensor): example IDs in the original input order
                - `ntokens` (int): total number of tokens in the batch
                - `net_input` (dict): the input to the Model, containing keys:
                  - `src_tokens` (LongTensor): a padded 2D Tensor of tokens in
                    the source sentence of shape `(bsz, src_len)`.
                  - `src_lengths` (LongTensor): 1D Tensor of the unpadded
                    lengths of each source sentence of shape `(bsz)`
                  - `prev_output_tokens` (LongTensor): a padded 2D Tensor of
                    tokens in the target sentence, shifted right by one
                    position for teacher forcing, of shape `(bsz, tgt_len)`.
                  - `lengths` (LongTensor): 1D Tensor of the unpadded
                    lengths of each target sentence of shape `(bsz)`
        """
        res = collate(
            samples, 
            pad_idx=self.dict.pad(),
            eos_idx=self.dict.eos(),
            prefix=self.prefix,
            sep_idx=self.dict.sep_index,
            prompt=self.prompt,
        )
        return res

    def num_tokens(self, index):
        """Return the number of tokens in a sample. This value is used to
        enforce ``--max-tokens`` during batching."""
        return self.sizes[index]

    def num_tokens_vec(self, indices):
        """Return the number of tokens for a set of positions defined by indices.
        This value is used to enforce ``--max-tokens`` during batching."""
        sizes = self.sizes[indices]
        return sizes

    def size(self, index):
        """Return an example's size as a float or tuple. This value is used when
        filtering a dataset with ``--max-positions``."""
        return self.sizes[index]

    def ordered_indices(self):
        """Return an ordered list of indices. Batches will be constructed based
        on this order."""
        if self.shuffle:
            indices = np.random.permutation(len(self)).astype(np.int64)
        else:
            indices = np.arange(len(self), dtype=np.int64)
        return indices[np.argsort(self.sizes[indices], kind="mergesort")]

    @property
    def supports_prefetch(self):
        return getattr(self.src, "supports_prefetch", False) and (
            getattr(self.tgt, "supports_prefetch", False) or self.tgt is None
        )

    def prefetch(self, indices):
        self.src.prefetch(indices)
        self.tgt.prefetch(indices)

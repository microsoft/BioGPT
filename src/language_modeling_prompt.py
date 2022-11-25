# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import logging
import os
from dataclasses import dataclass, field
from typing import Optional

import torch
from fairseq import search, utils
from fairseq.data import (
    Dictionary,
    data_utils,
    indexed_dataset,
)

from fairseq.tasks import register_task
from fairseq.tasks.language_modeling import LanguageModelingConfig, LanguageModelingTask
from .language_model_prompt_dataset import LanguageModelPromptDataset
from omegaconf import II


logger = logging.getLogger(__name__)


@dataclass
class LanguageModelingPromptConfig(LanguageModelingConfig):
    source_lang: Optional[str] = field(
        default=None, metadata={"help": "source language", "argparse_alias": "-s",}
    )
    target_lang: Optional[str] = field(
        default=None, metadata={"help": "target language","argparse_alias": "-t",}
    )
    max_source_positions: Optional[int] = field(
        default=384, metadata={"help": "max number of tokens in the source sequence, exclude eos."}
    )
    manual_prompt: Optional[str] = field(
        default=None, metadata={"help": "manual prompt to use",}
    )
    learned_prompt: Optional[int] = field(
        default=None, metadata={"help": "number of virtual tokens to use",}
    )
    learned_prompt_pattern: Optional[str] = field(
        default='learned', metadata={"help": "pattern of virtual tokens, default is learned",}
    )
    prefix: Optional[bool] = field(
        default=False, metadata={"help": "whether put prompt as prefix."}
    )
    sep_token: Optional[str] = field(
        default="<seqsep>", metadata={"help": "token to seperate prompt source and target."}
    )


@register_task("language_modeling_prompt", dataclass=LanguageModelingPromptConfig)
class LanguageModelingPromptTask(LanguageModelingTask):
    """
    Train a language model.

    Args:
        dictionary (~fairseq.data.Dictionary): the dictionary for the input of
            the language model
        output_dictionary (~fairseq.data.Dictionary): the dictionary for the
            output of the language model. In most cases it will be the same as
            *dictionary*, but could possibly be a more limited version of the
            dictionary (if ``--output-dictionary-size`` is used).
        targets (List[str]): list of the target types that the language model
            should predict.  Can be one of "self", "future", and "past".
            Defaults to "future".

    .. note::

        The language modeling task is compatible with :mod:`fairseq-train`,
        :mod:`fairseq-generate`, :mod:`fairseq-interactive` and
        :mod:`fairseq-eval-lm`.

    The language modeling task provides the following additional command-line
    arguments:

    .. argparse::
        :ref: fairseq.tasks.language_modeling_parser
        :prog:
    """
    def __init__(self, args, dictionary, output_dictionary=None, prompt=None, targets=None):
        super().__init__(args, dictionary, output_dictionary, targets)
        self.prompt = prompt
        self.prompt_length = self.prompt.size(0) if self.prompt is not None else 0
        self.prefix = args.prefix

    @classmethod
    def setup_prompt(cls, args, dictionary):
        if args.prefix:
            dictionary.sep_index = dictionary.add_symbol(args.sep_token)
        else:
            dictionary.sep_index = None
        assert not (args.manual_prompt and args.learned_prompt), "manual prompt and learned prompt can not be set "
        if args.manual_prompt and len(args.manual_prompt) != 0:
            prompt = dictionary.encode_line(args.manual_prompt, append_eos=False).long()
        elif args.learned_prompt:
            prompt = ''
            for idx in range(args.learned_prompt):
                prompt += args.learned_prompt_pattern + str(idx+1) + ' '
            prompt = dictionary.encode_line(prompt, append_eos=False).long()
        else:
            prompt = None
        return prompt

    @classmethod
    def setup_dictionary(cls, args, **kwargs):
        dictionary = None
        output_dictionary = None
        if args.data:
            paths = utils.split_paths(args.data)
            assert len(paths) > 0
            dictionary = Dictionary.load(os.path.join(paths[0], "dict.{}.txt".format(args.source_lang)))
            logger.info("dictionary: {} types".format(len(dictionary)))
            #output_dictionary = Dictionary.load(os.path.join(paths[0], "dict.{}.txt".format(args.target_lang)))
            output_dictionary = dictionary
        return (dictionary, output_dictionary)

    @classmethod
    def setup_task(cls, args, **kwargs):
        """Setup the task (e.g., load dictionaries).

        Args:
            args (argparse.Namespace): parsed command-line arguments
        """
        paths = utils.split_paths(args.data)
        assert len(paths) > 0
        # find language pair automatically
        if args.source_lang is None or args.target_lang is None:
            args.source_lang, args.target_lang = data_utils.infer_language_pair(paths[0])
        if args.source_lang is None or args.target_lang is None:
            raise Exception(
                "Could not infer language pair, please provide it explicitly"
            )

        dictionary, output_dictionary = cls.setup_dictionary(args, **kwargs)
        prompt = cls.setup_prompt(args, dictionary)

        # upgrade old checkpoints
        if getattr(args, "exclude_self_target", False):
            args.self_target = False

        targets = []
        if getattr(args, "self_target", False):
            targets.append("self")
        if getattr(args, "future_target", False):
            targets.append("future")
        if getattr(args, "past_target", False):
            targets.append("past")
        if len(targets) == 0:
            # standard language modeling
            targets = ["future"]

        return cls(args, dictionary, output_dictionary, prompt, targets=targets)

    def load_dataset(
        self, split: str, epoch=1, combine=False, **kwargs
    ) -> LanguageModelPromptDataset:
        """Load a given dataset split.

        Args:
            split (str): name of the split (e.g., train, valid, test)
        """
        def split_exists(split, src, tgt, lang, data_path):
            filename = os.path.join(data_path, "{}.{}-{}.{}".format(split, src, tgt, lang))
            return indexed_dataset.dataset_exists(filename, impl=self.args.dataset_impl)

        paths = utils.split_paths(self.args.data)
        assert len(paths) > 0
        data_path = paths[(epoch - 1) % len(paths)]

        # source
        if split_exists(split, self.args.source_lang, self.args.target_lang, self.args.source_lang, data_path):
            prefix = os.path.join(data_path, "{}.{}-{}.".format(split, self.args.source_lang, self.args.target_lang))
        else:
            raise FileNotFoundError(
                    "Dataset not found: {} ({})".format(split, data_path)
                )
        src_dataset = data_utils.load_indexed_dataset(
            prefix + self.args.source_lang, self.dictionary, self.args.dataset_impl
        )

        tgt_dataset = data_utils.load_indexed_dataset(
                prefix + self.args.target_lang, self.output_dictionary, self.args.dataset_impl
        )

        src_sizes = src_dataset.sizes
        tgt_sizes = tgt_dataset.sizes

        dataset = LanguageModelPromptDataset(
            src_dataset,
            src_sizes,
            self.dictionary,
            tgt_dataset,
            tgt_sizes,
            prefix = self.prefix,
            prompt=self.prompt,
            max_source_length=self.args.max_source_positions,
            max_length=self.args.max_target_positions,
            prompt_length=self.prompt_length
        )

        self.datasets[split] = dataset

    def build_dataset_for_inference(self, src_tokens, src_lengths, tgt_tokens=None, tgt_lengths=None):
        """
        Generate batches for inference. We prepend an eos token to src_tokens
        (or bos if `--add-bos-token` is set) and we append a <pad> to target.
        This is convenient both for generation with a prefix and LM scoring.
        """
        bs = len(src_tokens)
        if tgt_tokens is None:
            tgt_tokens = [torch.LongTensor([self.dictionary.eos()]) for _ in range(bs)]
            tgt_lengths = torch.LongTensor([t.numel() for t in tgt_tokens])
            
        dataset = LanguageModelPromptDataset(
            src_tokens,
            src_lengths,
            self.dictionary,
            tgt_tokens,
            tgt_lengths,
            prefix = self.prefix,
            prompt=self.prompt,
            max_source_length=self.args.max_source_positions,
            max_length=self.args.max_target_positions,
            prompt_length=self.prompt_length
        )

        return dataset
    
    def inference_step(self, generator, models, sample, prefix_tokens=None, constraints=None, allowed_text=None):
        with torch.no_grad():
            # Generation will always be conditioned on bos_token
            if getattr(self.args, "add_bos_token", False):
                bos_token = self.source_dictionary.bos()
            else:
                bos_token = self.source_dictionary.eos()

            if constraints is not None:
                raise NotImplementedError(
                    "Constrained decoding with the language_modeling task is not supported"
                )

            if allowed_text is not None:
                allowed_text = self.target_dictionary.encode_line(allowed_text, add_if_not_exist=False).to(sample['net_input']['src_tokens'])
            # SequenceGenerator doesn't use src_tokens directly, we need to
            # pass the `prefix_tokens` argument instead
        
            if prefix_tokens is None and sample["net_input"]["src_tokens"].nelement():
                prefix_tokens = sample["net_input"]["src_tokens"]
                if prefix_tokens[:, 0].eq(bos_token).all():
                    prefix_tokens = prefix_tokens[:, 1:]

            return generator.generate(
                models, sample, prefix_tokens=prefix_tokens, bos_token=bos_token, allowed_text=allowed_text
            )

    def build_generator(
        self, models, args, seq_gen_cls=None, extra_gen_cls_kwargs=None, prefix_allowed_tokens_fn=None
    ):
        from .constrained_generator import ConstrainedGenerator

        # Choose search strategy. Defaults to Beam Search.
        sampling = getattr(args, "sampling", False)
        sampling_topk = getattr(args, "sampling_topk", -1)
        sampling_topp = getattr(args, "sampling_topp", -1.0)
        diverse_beam_groups = getattr(args, "diverse_beam_groups", -1)
        diverse_beam_strength = getattr(args, "diverse_beam_strength", 0.5)
        match_source_len = getattr(args, "match_source_len", False)
        diversity_rate = getattr(args, "diversity_rate", -1)
        constrained = getattr(args, "constraints", False)
        if prefix_allowed_tokens_fn is None:
            prefix_allowed_tokens_fn = getattr(args, "prefix_allowed_tokens_fn", None)
        if (
            sum(
                int(cond)
                for cond in [
                    sampling,
                    diverse_beam_groups > 0,
                    match_source_len,
                    diversity_rate > 0,
                ]
            )
            > 1
        ):
            raise ValueError("Provided Search parameters are mutually exclusive.")
        assert sampling_topk < 0 or sampling, "--sampling-topk requires --sampling"
        assert sampling_topp < 0 or sampling, "--sampling-topp requires --sampling"

        if sampling:
            search_strategy = search.Sampling(
                self.target_dictionary, sampling_topk, sampling_topp
            )
        elif diverse_beam_groups > 0:
            search_strategy = search.DiverseBeamSearch(
                self.target_dictionary, diverse_beam_groups, diverse_beam_strength
            )
        elif match_source_len:
            # this is useful for tagging applications where the output
            # length should match the input length, so we hardcode the
            # length constraints for simplicity
            search_strategy = search.LengthConstrainedBeamSearch(
                self.target_dictionary,
                min_len_a=1,
                min_len_b=0,
                max_len_a=1,
                max_len_b=0,
            )
        elif diversity_rate > -1:
            search_strategy = search.DiverseSiblingsSearch(
                self.target_dictionary, diversity_rate
            )
        elif constrained:
            search_strategy = search.LexicallyConstrainedBeamSearch(
                self.target_dictionary, args.constraints
            )
        elif prefix_allowed_tokens_fn:
            search_strategy = search.PrefixConstrainedBeamSearch(
                self.target_dictionary, prefix_allowed_tokens_fn
            )
        else:
            search_strategy = search.BeamSearch(self.target_dictionary)

        extra_gen_cls_kwargs = extra_gen_cls_kwargs or {}
        
        seq_gen_cls = ConstrainedGenerator

        return seq_gen_cls(
            models,
            self.target_dictionary,
            beam_size=getattr(args, "beam", 5),
            max_len_a=getattr(args, "max_len_a", 0),
            max_len_b=getattr(args, "max_len_b", 200),
            min_len=getattr(args, "min_len", 1),
            normalize_scores=(not getattr(args, "unnormalized", False)),
            len_penalty=getattr(args, "lenpen", 1),
            unk_penalty=getattr(args, "unkpen", 0),
            temperature=getattr(args, "temperature", 1.0),
            match_source_len=getattr(args, "match_source_len", False),
            no_repeat_ngram_size=getattr(args, "no_repeat_ngram_size", 0),
            search_strategy=search_strategy,
            **extra_gen_cls_kwargs,
        )

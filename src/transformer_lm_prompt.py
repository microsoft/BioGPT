# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import logging
from dataclasses import dataclass, field
from typing import Optional, Dict, List, Tuple
from argparse import Namespace
import torch
from torch import Tensor
import torch.nn as nn
import torch.nn.functional as F

from fairseq import options, utils
from fairseq.dataclass import ChoiceEnum, FairseqDataclass
from fairseq.models import (
    FairseqLanguageModel,
    register_model,
    register_model_architecture,
)
from fairseq.models.transformer import (
    DEFAULT_MIN_PARAMS_TO_WRAP, Embedding, TransformerDecoder
)
from fairseq.modules import AdaptiveInput, CharacterTokenEmbedder
from fairseq.dataclass.utils import convert_namespace_to_omegaconf
from fairseq.models.transformer_lm import (
    TransformerLanguageModelConfig,
    TransformerLanguageModel, 
    transformer_lm_gpt2_small,
    transformer_lm_gpt2_big,
)
from omegaconf import II, DictConfig


logger = logging.getLogger(__name__)


@register_model("transformer_lm_prompt", dataclass=TransformerLanguageModelConfig)
class TransformerLanguageModelPrompt(TransformerLanguageModel):

    def load_state_dict(
        self,
        state_dict,
        strict=True,
        model_cfg: Optional[DictConfig] = None,
        args: Optional[Namespace] = None,
    ):
        """Copies parameters and buffers from *state_dict* into this module and
        its descendants.

        Overrides the method in :class:`nn.Module`. Compared with that method
        this additionally "upgrades" *state_dicts* from old checkpoints.
        """

        if model_cfg is None and args is not None:
            logger.warn("using 'args' is deprecated, please update your code to use dataclass config")
            model_cfg = convert_namespace_to_omegaconf(args).model

        self.upgrade_state_dict(state_dict)

        device = state_dict["decoder.embed_tokens.weight"].device
        if self.decoder.embed_tokens.weight.shape[0] > state_dict["decoder.embed_tokens.weight"].shape[0]:
            shape = state_dict["decoder.embed_tokens.weight"].shape
            state_dict["decoder.embed_tokens.weight"] = torch.cat(
                [state_dict["decoder.embed_tokens.weight"],
                self.decoder.embed_tokens.weight[shape[0]:].to(device)]
            )
        if self.decoder.output_projection.weight.shape[0] > state_dict["decoder.output_projection.weight"].shape[0]:
            shape = state_dict["decoder.output_projection.weight"].shape
            device = state_dict["decoder.output_projection.weight"].device
            state_dict["decoder.output_projection.weight"] = torch.cat(
                [state_dict["decoder.output_projection.weight"],
                self.decoder.output_projection.weight[shape[0]:].to(device)]
            )

        from fairseq.checkpoint_utils import prune_state_dict

        new_state_dict = prune_state_dict(state_dict, model_cfg)
        return super().load_state_dict(new_state_dict, strict)


@register_model_architecture("transformer_lm_prompt", "transformer_lm_prompt_biogpt")
def transformer_lm_prompt_biogpt(args):
    transformer_lm_gpt2_small(args)

@register_model_architecture("transformer_lm_prompt", "transformer_lm_prompt_biogpt_large")
def transformer_lm_prompt_gpt2_big(args):
    transformer_lm_gpt2_big(args)
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

SAVE_DIR=../../../checkpoints/QA-PubMedQA-BioGPT-Large-ReasoningFree
mkdir -p ${SAVE_DIR}

fairseq-train \
    ../../../data/PubMedQA/pqal_qcal-biogpt-large-ansis-bin --save-dir ${SAVE_DIR} \
    --user-dir ../../src \
    --finetune-from-model ../../../checkpoints/Pre-trained-BioGPT-Large/checkpoint.pt \
    --task language_modeling_prompt \
    --arch transformer_lm_prompt_biogpt_large \
    --share-decoder-input-output-embed --decoder-learned-pos \
    --optimizer adam --adam-betas '(0.9, 0.98)' \
    --weight-decay 0.01 --clip-norm 0.0 \
    --lr 1e-5 --lr-scheduler inverse_sqrt --warmup-updates 100 --warmup-init-lr 1e-07 \
    --tokens-per-sample 2048 --max-source-positions 1900 --max-target-positions 2048 \
    --max-tokens 2048 --update-freq 16 \
    --skip-invalid-size-inputs-valid-test \
    --max-epoch 100 --keep-last-epochs 5 \
    --learned-prompt 9
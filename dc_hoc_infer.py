import torch
from src.transformer_lm_prompt import TransformerLanguageModelPrompt


src_text = "These results indicate that while both preparations of Apo2L/TRAIL possess biological activity , there are important differences as regards their ability to induce apoptosis in normal and immortalized keratinocytes ."

m = TransformerLanguageModelPrompt.from_pretrained(
        "checkpoints/DC-HoC-BioGPT",
        "checkpoint_last.pt",
        "data/HoC/ansis-bin",
        tokenizer='moses',
        bpe='fastbpe',
        bpe_codes="data/bpecodes",
        min_len=100,
        max_len_b=1024)

#m.cuda()

src_tokens = m.encode(src_text)
generate = m.generate([src_tokens], beam=1)[0]
#output = m.decode(generate[0]["tokens"]).replace("learned1", "").split("the type of this document is ")
split_output = m.decode(generate[0]["tokens"]).split("learned1")[1:]
output = " ".join(split_output)

print(output)








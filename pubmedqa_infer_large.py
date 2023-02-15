import torch
from src.transformer_lm_prompt import TransformerLanguageModelPrompt


src_text = "question: is anorectal endosonography valuable in dyschesia? context: dyschesia can be provoked by inappropriate defecation movements. the aim of this prospective study was to demonstrate dysfunction of the anal sphincter and/or the musculus (m.) puborectalis in patients with dyschesia using anorectal endosonography. twenty consecutive patients with a medical history of dyschesia and a control group of 20 healthy subjects underwent linear anorectal endosonography (toshiba models iuv 5060 and pvl-625 rt). in both groups, the dimensions of the anal sphincter and the m. puborectalis were measured at rest, and during voluntary squeezing and straining. statistical analysis was performed within and between the two groups. the anal sphincter became paradoxically shorter and/or thicker during straining (versus the resting state) in 85% of patients but in only 35% of control subjects. changes in sphincter length were statistically significantly different (p<0.01, chi(2) test) in patients compared with control subjects. the m. puborectalis became paradoxically shorter and/or thicker during straining in 80% of patients but in only 30% of controls. both the changes in length and thickness of the m. puborectalis were significantly different (p<0.01, chi(2) test) in patients versus control subjects. answer: linear anorectal endosonography demonstrated incomplete or even absent relaxation of the anal sphincter and the m. puborectalis during a defecation movement in the majority of our patients with dyschesia. this study highlights the value of this elegant ultrasonographic technique in the diagnosis of pelvic floor dyssynergia or anismus."

m = TransformerLanguageModelPrompt.from_pretrained(
        "checkpoints/QA-PubMedQA-BioGPT-Large",
        "checkpoint_avg.pt",
        "data/PubMedQA/biogpt-large-ansis-bin",
        tokenizer='moses',
        bpe='fastbpe',
        bpe_codes="data/BioGPT-Large/bpecodes",
        min_len=100,
        max_len_b=1024,
        beam=1)

m.cuda()

src_tokens = m.encode(src_text)
generate = m.generate([src_tokens], beam=1)[0]
output = m.decode(generate[0]["tokens"]).split("learned9")[-1]

print(output)
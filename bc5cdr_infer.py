import torch
from src.transformer_lm_prompt import TransformerLanguageModelPrompt

m = TransformerLanguageModelPrompt.from_pretrained(
        "checkpoints/RE-BC5CDR-BioGPT",
        "checkpoint_avg.pt", 
        "data/BC5CDR/relis-bin",
        tokenizer='moses', 
        bpe='fastbpe', 
        bpe_codes="data/bpecodes",
        max_len_b=1024,
        beam=1)

#m.cuda()

#src_text = "tricuspid valve regurgitation and lithium carbonate toxicity in a newborn infant. a newborn with massive tricuspid regurgitation, atrial flutter, congestive heart failure, and a high serum lithium level is described. this is the first patient to initially manifest tricuspid regurgitation and atrial flutter, and the 11th described patient with cardiac disease among infants exposed to lithium compounds in the first trimester of pregnancy. sixty-three percent of these infants had tricuspid valve involvement. lithium carbonate may be a factor in the increasing incidence of congenital heart disease when taken during early pregnancy. it also causes neurologic depression, cyanosis, and cardiac arrhythmia when consumed prior to delivery."
src_text = "phenobarbital-induced dyskinesia in a neurologically-impaired child. a 2-year-old child with known neurologic impairment developed a dyskinesia soon after starting phenobarbital therapy for seizures. known causes of movement disorders were eliminated after evaluation. on repeat challenge with phenobarbital, the dyskinesia recurred. phenobarbital should be added to the list of anticonvulsant drugs that can cause movement disorders."
src_tokens = m.encode(src_text)
generate = m.generate([src_tokens], beam=5)[0]
output = m.decode(generate[0]["tokens"])
stripped_output = output.split("learned9")[-1]

print(stripped_output)

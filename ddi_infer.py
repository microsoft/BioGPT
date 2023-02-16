import torch
from src.transformer_lm_prompt import TransformerLanguageModelPrompt

m = TransformerLanguageModelPrompt.from_pretrained(
        "checkpoints/RE-DDI-BioGPT",
        "checkpoint_avg.pt", 
        "data/DDI/relis-bin",
        tokenizer='moses', 
        bpe='fastbpe', 
        bpe_codes="data/bpecodes",
        max_len_b=1024,
        beam=1)

#m.cuda()

#src_text = "Digitalis toxicity may be aggravated by the initial release of norepinephrine caused by Bretylium Tosylate Injection. The pressor effects of catecholamines such as dopamine or norepinephrine are enhanced by Bretylium Tosylate. When catecholamines are administered, dilute solutions should be used and blood pressure should be monitored closely. Although there is little published information on concomitant administration of lidocaine and Bretylium Tosylate, these drugs are often administered concurrently without any evidence of interactions resulting in adverse effects or diminished efficacy."
src_text = "Chlorthalidone may add to or potentiate the action of other antihypertensive drugs. Potentiation occurs with ganglionic peripheral adrenergic blocking drugs. Medication such as digitalis may also influence serum electrolytes. Warning signs, irrespective of cause, are: dryness of mouth, thirst, weakness, lethargy, drowsiness, restlessness, muscle pains or cramps, muscular fatigue, hypotension, oliguria, tachycardia, and gastrointestinal disturbances such as nausea and vomiting. Insulin requirements in diabetic patients may be increased, decreased, or unchanged. Higher dosage of oral hypoglycemic agents may be required. Latent diabetes mellitus may become manifest during chlorthalidone administration. Chlorthalidone and related drugs may increase the responsiveness to tubocurarine. Chlorthalidone and related drugs may decrease arterial responsiveness to norepinephrine. This diminution is not sufficient to preclude effectiveness of the pressor agent for therapeutic use."
src_tokens = m.encode(src_text)
generate = m.generate([src_tokens], beam=5)[0]
output = m.decode(generate[0]["tokens"])
stripped_output = output.split("learned9")[-1]

print(stripped_output)

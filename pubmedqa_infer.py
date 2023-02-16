import torch
from src.transformer_lm_prompt import TransformerLanguageModelPrompt


src_text = "question: Is cytokeratin immunoreactivity useful in the diagnosis of short-segment Barrett's oesophagus in Korea? context: Cytokeratin 7/20 staining has been reported to be helpful in diagnosing Barrett's oesophagus and gastric intestinal metaplasia. However, this is still a matter of some controversy. To determine the diagnostic usefulness of cytokeratin 7/20 immunostaining for short-segment Barrett's oesophagus in Korea. In patients with Barrett's oesophagus, diagnosed endoscopically, at least two biopsy specimens were taken from just below the squamocolumnar junction. If goblet cells were found histologically with alcian blue staining, cytokeratin 7/20 immunohistochemical stains were performed. Intestinal metaplasia at the cardia was diagnosed whenever biopsy specimens taken from within 2 cm below the oesophagogastric junction revealed intestinal metaplasia. Barrett's cytokeratin 7/20 pattern was defined as cytokeratin 20 positivity in only the superficial gland, combined with cytokeratin 7 positivity in both the superficial and deep glands. Barrett's cytokeratin 7/20 pattern was observed in 28 out of 36 cases (77.8%) with short-segment Barrett's oesophagus, 11 out of 28 cases (39.3%) with intestinal metaplasia at the cardia, and nine out of 61 cases (14.8%) with gastric intestinal metaplasia. The sensitivity and specificity of Barrett's cytokeratin 7/20 pattern were 77.8 and 77.5%, respectively. answer: Barrett's cytokeratin 7/20 pattern can be a useful marker for the diagnosis of short-segment Barrett's oesophagus, although the false positive or false negative rate is approximately 25%."

m = TransformerLanguageModelPrompt.from_pretrained(
        "checkpoints/QA-PubMedQA-BioGPT",
        "checkpoint_avg.pt",
        "data/PubMedQA/ansis-bin",
        tokenizer='moses',
        bpe='fastbpe',
        bpe_codes="data/bpecodes",
        min_len=100,
        max_len_b=1024)

#m.cuda()

src_tokens = m.encode(src_text)
generate = m.generate([src_tokens], beam=1)[0]
output = m.decode(generate[0]["tokens"]).split("learned9")[-1]

print(output)














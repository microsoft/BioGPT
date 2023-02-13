import torch
from src.transformer_lm_prompt import TransformerLanguageModelPrompt

m = TransformerLanguageModelPrompt.from_pretrained(
        "checkpoints/RE-DTI-BioGPT", 
        "checkpoint_avg.pt", 
        "data/KD-DTI/relis-bin",
        tokenizer='moses', 
        bpe='fastbpe', 
        bpe_codes="data/bpecodes",
        max_len_b=1024,
        beam=1)

#m.cuda()

#src_text="Piglet saphenous vein contains multiple relaxatory prostanoid receptors: evidence for EP4, EP2, DP and IP receptor subtypes. Prostaglandin E(2) produced endothelium-independent relaxation of phenylephrine- and 5-HT-contracted piglet saphenous vein (PSV; pEC(50)=8.6+/-0.2; n=6). The prostanoid EP(4) receptor antagonist GW627368X (30-300 nM) produced parallel rightward displacement of PGE(2) concentration-effect (E/[A]) curves (pK(b)=9.2+/-0.2; slope=1). Higher concentrations of GW627368X did not produce further rightward shifts, revealing the presence of non-EP(4) prostanoid receptors. In all, 18 other prostanoid receptor agonists relaxed PSV in a concentration-related manner. Relative potencies of agonists most sensitive to 10 muM GW627368X (and therefore predominantly activating EP(4) receptors) correlated well with those at human recombinant EP(4) receptors in human embryonic kidney (HEK-293) cells (r(2)=0.74). In the presence of 10 microM GW627368X, the rank order of agonist relative potency matched that of the human recombinant EP(2) receptor in Chinese hamster ovary cells (r(2)=0.72). Iloprost, cicaprost and PGI(2) relaxed PSV maximally and were antagonised by 10 microM GW627368X, demonstrating that they were full EP(4) receptor agonists. Residual responses to these compounds in the presence of GW627368X suggested the presence of IP receptors.BW245C relaxed PSV maximally (pEC(50)=6.8+/-0.1). In the presence of 10 microM GW627368X, BW245C produced biphasic E/[A] curves (phase one pEC(50)=6.6; alpha=24%; phase two pEC(50)=5.1; alpha=112%). Phase two was antagonised by the DP receptor antagonist BW A868C (1 microM), demonstrating that BW245C is an agonist at DP and EP4 receptors. We conclude that PSV contains EP(4), EP(2), DP and IP receptors; IP receptor agonists are also porcine EP(4) receptor agonists." # input text, e.g., a PubMed abstract
src_text = "Iodine-131 tositumomab (Bexxar): radioimmunoconjugate therapy for indolent and transformed B-cell non-Hodgkin's lymphoma. Tositumomab is an immunoglobulin G murine monoclonal antibody that binds to the CD20 antigen on the surface of normal and malignant human B-cells. Tositumomab is linked covalently with iodine-131 to produce the radioimmunoconjugate iodine-131 tositumomab (Bexxar). The iodine-131 tositumomab regimen was approved by the US Food and Drug Administration in June 2003 for the treatment of patients with CD20-positive, follicular non-Hodgkin's lymphoma, both with and without transformation, whose disease is refractory to rituximab (Rituxan) and has relapsed following chemotherapy. The dose-limiting toxicity of iodine-131 tositumomab is bone marrow suppression and resulting cytopenias. Unlike chemotherapy, the majority of nonhematologic adverse events associated with iodine-131 tositumomab are mild to moderate in nature and usually self limited. Iodine-131 tositumomab represents one of the most active single agents for the treatment of recurrent indolent and transformed B-cell non-Hodgkin's lymphoma, as demonstrated by several clinical trials summarized in this review. At the present time, the use of radioimmunoconjugate therapy is largely limited to patients with disease refractory to rituximab therapy and transformed disease not amenable to high-dose therapy and autologous stem cell support. Longer follow-up of ongoing clinical trials should provide reassurance as to safety and insights as to the additive stem cell toxicity from iodine-131 tositumomab administration. Studies are also addressing the role of iodine-131 tositumomab as a component of initial therapy for indolent non-Hodgkin's lymphoma and in additional histologies of non-Hodgkin's lymphoma." # input text, e.g., a PubMed abstract
src_tokens = m.encode(src_text)
generate = m.generate([src_tokens], beam=5)[0]
output = m.decode(generate[0]["tokens"])
stripped_output = output.split("learned9")[-1]

print(stripped_output)

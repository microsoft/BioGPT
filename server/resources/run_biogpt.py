from fairseq.models.transformer_lm import TransformerLanguageModel
from flask import request
from flask_restful import Resource


class RunBioGptApi(Resource):
    def post(self):
        question = request.json.get('question')
        m = TransformerLanguageModel.from_pretrained(
            "checkpoints/Pre-trained-BioGPT",
            "checkpoint.pt",
            "data",
            tokenizer='moses',
            bpe='fastbpe',
            bpe_codes="data/bpecodes",
            min_len=100,
            max_len_b=1024)
        m.cuda()
        src_tokens = m.encode(question)
        generate = m.generate([src_tokens], beam=5)[0]
        answer = m.decode(generate[0]["tokens"])
        return {"answer": answer}

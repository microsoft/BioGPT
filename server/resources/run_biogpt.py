from flask import request
from flask_restful import Resource

from server.config import Config
from server.resources.models import *

MODEL_CONFIGS = {
    "ddi": DDI,
    "dti": DTI,
    "bc5cdr": BC5CDR,
    "document_classification": DocumentClassification,
    "pubmed": Pubmed,
    "pubmed_large": PubmedLarge,
    "pretrained_biogpt": PretrainedBioGPT,
    "pretrained_biogpt_large": PretrainedBioGPTLarge
}


class RunBioGptApi(Resource):

    def post(self):
        question = request.json.get('question')
        model_name = request.json.get('model_name')
        beam = request.json.get('beam')
        if not beam:
            beam = 5
        else:
            beam = int(beam)
        model = MODEL_CONFIGS[model_name]()
        m = model.m

        config = Config()
        if not config.local_depployment:
            m.cuda()
        if model_name == "pretrained_biogpt_large" and not config.local_depployment:
            m.half()

        src_tokens = m.encode(question)
        generate = m.generate([src_tokens], beam=beam)[0]
        answer = m.decode(generate[0]["tokens"])

        cleaned_answer = model.clean_output(answer)
        return {"answer": cleaned_answer}

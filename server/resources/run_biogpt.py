
from flask import request
from flask_restful import Resource

from server.resources.pre_trained_biogpt import Models


class RunBioGptApi(Resource):
    def post(self):
        question = request.json.get('question')
        m = Models().trained_biogpt
        # m.cuda()
        src_tokens = m.encode(question)
        generate = m.generate([src_tokens], beam=5)[0]
        answer = m.decode(generate[0]["tokens"])
        return {"answer": answer}

from flask_restful import Resource


class RunBioGptApi(Resource):
    def post(self):
        print('hello world')

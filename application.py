from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_bcrypt import Bcrypt

from server.log import set_logging
from server.resources.pre_trained_biogpt import Models
from server.routes import init_routes

application = Flask(__name__)
CORS = CORS(application)
API = Api(application)
bcrypt = Bcrypt(application)

init_routes(API)
set_logging(application)

if __name__ == "__main__":
    # pre-load all models to speed up the request calculation time
    _ = Models()
    application.run(host='0.0.0.0', port=8001)

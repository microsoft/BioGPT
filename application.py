from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_bcrypt import Bcrypt

from server.config import Config
from server.log import set_logging
from server.resources.models import *
from server.routes import init_routes

application = Flask(__name__)
CORS = CORS(application)
API = Api(application)
bcrypt = Bcrypt(application)

init_routes(API)
set_logging(application)

if __name__ == "__main__":
    # pre-load all models and config to speed up the request calculation time
    # _ = DDI(),
    # _ = DTI(),
    # _ = BC5CDR(),
    # _ = DocumentClassification(),
    # _ = Pubmed(),
    # _ =  PubmedLarge(),
    _ = PretrainedBioGPT(),
    # _ = PretrainedBioGPTLarge()

    _ = Config()
    application.run(host='0.0.0.0', port=8001)

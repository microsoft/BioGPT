import os

from server.utils import singleton


@singleton
class Config:
    def __init__(self):
        self.local_depployment = os.environ.get('LOCAL_DEPLOYMENT').lower() == 'true'

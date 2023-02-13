import logging
import os

from logging.handlers import RotatingFileHandler


def set_logging(application):
    formatter = logging.Formatter(
            "%(asctime)s  [%(levelname)s]\n%(message)s",
            "%Y-%m-%d %H:%M:%S"
    )

    flask_handler = RotatingFileHandler(
        'server.log',
        maxBytes=1000000,
        backupCount=5
    )
    flask_handler.setFormatter(formatter)
    flask_handler.setLevel(os.environ.get("LOGLEVEL", "DEBUG"))
    application.logger.addHandler(flask_handler)

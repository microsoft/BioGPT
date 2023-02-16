import logging
import os

from logging.handlers import RotatingFileHandler


def set_logging(application):
    file = 'server.log'
    formatter = logging.Formatter(
            "%(asctime)s  [%(levelname)s]\n%(message)s",
            "%Y-%m-%d %H:%M:%S"
    )

    # Create log file if doesn't exist
    open(file, 'w+').close()

    flask_handler = RotatingFileHandler(
        file,
        maxBytes=1000000,
        backupCount=5
    )
    flask_handler.setFormatter(formatter)
    flask_handler.setLevel(os.environ.get("LOGLEVEL", "DEBUG"))
    application.logger.addHandler(flask_handler)

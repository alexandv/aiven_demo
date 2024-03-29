import json
import logging.config
from logging import INFO
import os

def setupLogging(
        path=r'config/log/logging.json',
        level=None,
        env_key='WATO_LOG_CFG'
    ):
    value = os.getenv(env_key, None)
    if value is not None:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
            if level is not None:
                config["root"]["level"] = level
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=INFO)

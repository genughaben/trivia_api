import logging
import os
import sys
from logging import Logger

logger: Logger

def init_logger_singleton():
    global logger

    logger = logging.getLogger(name='trivia_logger')
    if os.getenv('ENV') == 'debug':
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.ERROR)
    formatter = logging.Formatter(
        '[%(asctime)s:%(module)s:%(lineno)s:%(levelname)s] %(message)s'
    )
    streamhandler = logging.StreamHandler(sys.stdout)
    streamhandler.setLevel(logging.ERROR)
    streamhandler.setFormatter(formatter)
    logger.addHandler(streamhandler)
    filehandler = logging.FileHandler('trivia.log')
    filehandler.setLevel(logging.DEBUG)
    filehandler.setFormatter(formatter)
    logger.addHandler(filehandler)


init_logger_singleton()

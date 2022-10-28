import logging
from logging.handlers import RotatingFileHandler

from constants import LOGGER_DIR


def logger_conf():
    logger_dir = LOGGER_DIR
    logger_dir.mkdir(exist_ok=True)
    logger_file = logger_dir / 'task_1_logger.log'
    rotating_handler = RotatingFileHandler(
        logger_file,
        maxBytes=10**6,
        backupCount=5
    )
    logging.basicConfig(
        datefmt='%d.%m.%Y %H:%M:%S',
        format='"%(asctime)s - [%(levelname)s] - %(message)s"',
        level=logging.DEBUG,
        handlers=(rotating_handler, logging.StreamHandler())
    )

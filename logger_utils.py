import logging
import sys
from logging.handlers import TimedRotatingFileHandler

FORMATTER = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler(log_file):
    file_handler = TimedRotatingFileHandler(log_file)
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_logger(log_file, logger_name):
    logger = logging.getLogger(logger_name)
    
    logger.setLevel(logging.DEBUG)  # better to have too much log than not enough
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler(log_file))
    
    # with this pattern, it's rarely necessary to propagate the error up to parent
    logger.propagate = False
    
    return logger

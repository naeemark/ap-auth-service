"""
  App Universal logger
"""
import logging

import watchtower

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(watchtower.CloudWatchLogHandler())
logger.info("Hi")


def info(log_data):
    """ Logs info """
    logger.info(log_data)


def warn(log_data):
    """ Logs warn """
    logger.warning(log_data)


def error(log_data):
    """ Logs error """
    logger.error(log_data)

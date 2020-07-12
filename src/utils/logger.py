"""
  App Universal logger
"""
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("{}-{}".format(os.environ["MICROSERVICE_NAME"], os.environ["STAGE"]))


def info(log_data):
    """ Logs info """
    logger.info(log_data)


def warn(log_data):
    """ Logs warn """
    logger.warning(log_data)


def error(log_data):
    """ Logs error """
    logger.error(log_data)

import logging

from logger_extra.logger_context import get_logger_context
from logger_extra.utils import json_serialize


class LoggerContextFilter(logging.Filter):
  def __init__(self, name: str = ''):
    super().__init__(name)

  def filter(self, record: logging.LogRecord) -> bool:
    logger_context = get_logger_context()

    for key, value in logger_context.items():
      record.__dict__[key] = json_serialize(value)

    return True

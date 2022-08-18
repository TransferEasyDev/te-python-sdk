# -*- coding: utf-8 -*-

import logging
from config.__dev import (
    LOGGER_NAME, LOGGER_LEVEL_DEBUG,
    LOGGER_FORMATTER, LOGGER_EXTRA_HANDLER
)

logger = logging.getLogger(LOGGER_NAME)
_handler = logging.StreamHandler()
_formatter = logging.Formatter(LOGGER_FORMATTER)
_handler.setFormatter(_formatter)
logger.addHandler(_handler)
if LOGGER_LEVEL_DEBUG:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)
if LOGGER_EXTRA_HANDLER:
    pass

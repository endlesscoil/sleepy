#!/usr/bin/env python

import sys, os
import logging

from app.app import Player, Sleepy
from app.sources import PandoraSource, CherryMusicSource

class CustomFormatter(logging.Formatter):
    """Custom formatter, overrides funcName with value of name_override if it exists"""
    def format(self, record):
        if hasattr(record, 'name_override'):
            record.funcName = record.name_override
        return super(CustomFormatter, self).format(record)

rootlogger = logging.getLogger('')
rootlogger.setLevel(logging.DEBUG)
logging.getLogger("requests").setLevel(logging.WARNING)

fileHandler = logging.FileHandler('log.txt')
fileHandler.setFormatter(CustomFormatter('%(asctime)s - %(levelname)7s - %(name)20s:%(funcName)-15s - %(message)s'))
rootlogger.addHandler(fileHandler)

rootlogger.info('Starting up..')

sleepy = Sleepy()
sleepy._current_source.authenticate()

sleepy.next(autoplay=True)
sleepy.run()
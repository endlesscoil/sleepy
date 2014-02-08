#!/usr/bin/env python

import sys, os
import logging

from app.app import Player, Sleepy
from cherrymusicclient.api import api as cmapi
#from pandora import Pandora
from app.sources import PandoraSource, CherryMusicSource


#p = Player()
# source = PandoraSource()

# source.authenticate('', '')
# source.switch('Nuevo Flamenco')

# source = CherryMusicSource()
# source.url = ''
# source.authenticate('', '')
# source.switch('sleepy')

# sys.stderr.close()
# os.close(2)


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

############ CherryMusic
# cmapi.url = 'http://darkness:8080'
# cmapi.login('', '')
# sleepy_playlists = cmapi.show_playlists(filter='sleepy')
# playlist = cmapi.load_playlist(sleepy_playlists[0]['plid'])

# url = '{0}/serve/{1}'.format(cmapi.url, playlist[0]['urlpath'])

############ Pandora
# pandora = Pandora()

# pandora.authenticate('', '')

# use_station = None
# for station in pandora.stations:
# 	if station['stationName'] == 'Nuevo Flamenco':
# 		use_station = station

# pandora.switch_station(use_station)
# next = pandora.get_next_song()
# url = next['audioUrlMap']['highQuality']['audioUrl']

############ Common
# sleepy._player.url = url

# sleepy.play()
# while True:
# 	pass

# sleepy._console_ui.artist = 'Opeth'
# sleepy._console_ui.title = 'Blackwater Park'
# sleepy._console_ui.album = 'Blackwater Park'

#############

sleepy.next()
#sleepy._update_ui()
sleepy.play()
sleepy.run()
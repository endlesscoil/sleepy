import pygst
pygst.require('0.10')
import gst
import logging

from .interfaces import ConsoleUI, WebUI
from .sources import *
from .db import Session, Source
from .constants import SOURCES

class Sleepy(object):
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)7s - %(name)20s:%(funcName)-15s - %(message)s')

        logging.getLogger("requests").setLevel(logging.WARNING)

        self.log = logging.getLogger(self.__class__.__name__)
        self.log.info('Starting up..')

        self._session = Session()
        self._sources = Sources(self._session)
        self._current_source = self._sources.sources['CherryMusic']   # TEMP
        self._player = Player()

        self._console_ui = ConsoleUI()
        self._web_ui = WebUI()

    def run(self):
        self.log.info('Running..')
        self._console_ui.run()

    def play(self):
        self.log.info('Playing..')
        self._player.play()

    def stop(self):
        self.log.info('Stopping..')
        self._player.stop()

    def next(self):
        self.log.info('Getting next song..')
        url = self._current_source.next_song()
        self._player.url = url

        self._update_ui()
        self.play()

    def prev(self):
        pass

    def _update_ui(self):
        self.log.debug('Updating user interface..')
        song_info = self._current_source.song_info()

        self._console_ui.artist = song_info.artist
        self._console_ui.title = song_info.title
        self._console_ui.album = song_info.album

class Player(object):
    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)

        pulse = gst.element_factory_make("pulsesink", "pulse")
        fakesink = gst.element_factory_make("fakesink", "fakesink")

        self._player = gst.element_factory_make("playbin", "player")
        self._player.set_property('audio-sink', pulse)
        self._player.set_property('video-sink', fakesink)

        self._pipeline = gst.Pipeline("RadioPipe")
        self._pipeline.add(self._player)

    def play(self):
        self.log.debug('Setting state to PLAYING')
        self._pipeline.set_state(gst.STATE_PLAYING)

    def stop(self):
        self.log.debug('Setting state to PAUSED')
        self._pipeline.set_state(gst.STATE_PAUSED)

    @property
    def url(self):
        return self._url
    
    @url.setter
    def url(self, value):
        self._url = value
        self._player.set_property('uri', value)
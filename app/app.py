import pygst
pygst.require('0.10')
import gst

from .interfaces import ConsoleUI, WebUI
from .sources import CherryMusic, Pandora

class Sleepy(object):
    def __init__(self, source):
        self._source = source
        self._player = Player()

        self._console_ui = ConsoleUI()
        self._web_ui = WebUI()

    def run(self):
        self._console_ui.run()

    def play(self):
        self._player.play()

    def stop(self):
        self._player.stop()

    def next(self):
        pass

    def prev(self):
        pass

class Player(object):
    def __init__(self):
        pulse = gst.element_factory_make("pulsesink", "pulse")
        fakesink = gst.element_factory_make("fakesink", "fakesink")

        self._player = gst.element_factory_make("playbin", "player")
        self._player.set_property('audio-sink', pulse)
        self._player.set_property('video-sink', fakesink)

        self._pipeline = gst.Pipeline("RadioPipe")
        self._pipeline.add(self._player)

    def play(self):
        self._pipeline.set_state(gst.STATE_PLAYING)

    def stop(self):
        self._pipeline.set_state(gst.STATE_PAUSED)

    @property
    def url(self):
        return self._url
    
    @url.setter
    def url(self, value):
        self._url = value
        self._player.set_property('uri', value)
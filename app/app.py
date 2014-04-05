import pygst
pygst.require('0.10')

import gst
import logging

import gobject
gobject.threads_init()

from .interfaces import ConsoleUI, WebUI
from .sources import *
from .db import Session, Source
from .constants import SOURCES
from .decorators import log_method

class Sleepy(object):
    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)

        self._session = Session()
        self._sources = Sources(self._session)
        self._current_source = self._sources.sources['CherryMusic']   # TEMP
        self._player = Player(self)

        self._running = False
        self._console_ui = ConsoleUI(self)
        self._web_ui = WebUI()

    def run(self):
        self._running = True
        self.log.info('Running..')
        self._console_ui.run()

    def play(self):
        self.log.info('Playing..')
        self._player.play()

    def stop(self):
        self.log.info('Stopping..')
        self._player.stop()
        self._update_ui()

    def next(self, autoplay=False):
        self.log.info('Getting next song..')
        url = self._current_source.next_song()

        if autoplay:
            self.stop()

        if url:
            self._player.url = url
            if autoplay:
                self.play()
        else:
            self.log.info('Reached end of playlist')
    
    def prev(self):
        pass

    def _update_ui(self):
        if self._running:
            self.log.debug('Updating user interface..')
            song_info = self._current_source.song_info()

            self._console_ui.artist = song_info.artist
            self._console_ui.title = song_info.title
            self._console_ui.album = song_info.album

            self._console_ui.redraw()

class Player(object):
    def __init__(self, sleepy):
        self.sleepy = sleepy
        self.log = logging.getLogger(self.__class__.__name__)

        pulse = gst.element_factory_make("pulsesink", "pulse")

        self._player = gst.element_factory_make("playbin2", "player")
        self._player.set_property('audio-sink', pulse)

        self._pipeline = gst.Pipeline("RadioPipe")
        self._pipeline.add(self._player)

        self._bus = self._pipeline.get_bus()

        self._bus.enable_sync_message_emission()
        self._bus.add_signal_watch()
        self._bus.set_sync_handler(self._on_message)

        self._player.connect("about-to-finish", self.about_to_finish)
        #self._bus.connect('message', self._on_message)
        #self._bus.connect('stream_start', self.stream_start)

    @log_method
    def stream_start(self, player):
        pass

    @log_method        
    def about_to_finish(self, player):
        self.sleepy.next()

    @log_method
    def audio_changed(self, player):
        self.log.debug('audio changed')

    @log_method
    def play(self):
        self.log.debug('Setting state to PLAYING')
        self._pipeline.set_state(gst.STATE_PLAYING)

    @log_method
    def stop(self):
        self.log.debug('Setting state to NULL')
        self._pipeline.set_state(gst.STATE_NULL)

    @log_method
    def pause(self):
        self.log.debug('Setting state to PAUSE')
        self._pipeline.set_state(gst.STATE_PAUSE)

    @log_method
    def seek(self, location):
        try:
            self.log.info('Seeking to {0}'.format(location))
            event = gst.event_new_seek(1.0, gst.FORMAT_TIME, gst.SEEK_FLAG_FLUSH | gst.SEEK_FLAG_ACCURATE, 
                                        gst.SEEK_TYPE_SET, location, gst.SEEK_TYPE_NONE, 0)

            res = self._player.send_event(event)
            if res:
                self.log.info('setting stream time to 0')
                self._player.set_new_stream_time(0L)
            else:
                self.log.error('error seeking to {0}'.format(location))

        except Exception, err:
            self.log.error('Error: ' + str(err))

    def _on_message(self, bus, message):
        try:
            t = message.type

            if t == gst.MESSAGE_EOS:
                self.sleepy._console_ui.error = 'EOS'
                self.log.info('EOS')

            # elif t == gst.MESSAGE_STREAM_STATUS:
            #     #self.log.debug('stream status!')
            #     #status = message.parse_stream_status()
            #     #self.log.error(status[0].value_name, status[1])
            #     #self.sleepy._update_ui()

            elif t == gst.MESSAGE_DURATION:
                dur = message.parse_duration()

                if dur[0] == gst.FORMAT_TIME:
                    self.sleepy._update_ui()

            elif t == gst.MESSAGE_ERROR:
                err, debug = message.parse_error()

                self.log.error('gstreamer error: {0}'.format(err))

        except Exception, err:
            self.log.error(str(err))

        return gst.BUS_PASS

    @property
    def url(self):
        return self._url
    
    @url.setter
    def url(self, value):
        self._url = value
        self._player.set_property('uri', value)
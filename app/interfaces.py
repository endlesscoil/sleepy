import logging
import urwid
import threading

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
import tornado.autoreload

from .web import flask_app

class ConsoleUI(threading.Thread):
    def __init__(self, sleepy):
        threading.Thread.__init__(self)
        self.log = logging.getLogger(self.__class__.__name__)

        self.error_text = ''
        self._error = urwid.Text(u'')
        self.program_label = urwid.Text(u'Sleepy v0.1', align='center')
        self.artist_label = urwid.Text(u'Artist: ', align='right')
        self.artist_data = urwid.Text(u'', align='left')
        self.artist_box = urwid.Columns([self.artist_label, self.artist_data])
        self.title_label = urwid.Text(u'Title: ', align='right')
        self.title_data = urwid.Text(u'', align='left')
        self.title_box = urwid.Columns([self.title_label, self.title_data])
        self.album_label = urwid.Text(u'Album: ', align='right')
        self.album_data = urwid.Text(u'', align='left')
        self.album_box = urwid.Columns([self.album_label, self.album_data])
        self.divider = urwid.Divider()

        self.pile = urwid.Pile([self.program_label, self.divider, self.artist_box, self.title_box, self.album_box, self._error])

        self.bg = urwid.Filler(self.pile)
        self.loop = urwid.MainLoop(self.bg, unhandled_input=self._handle_input)

        self._sleepy = sleepy

    def run(self):
        self.loop.run()

    def redraw(self):
        self.loop.draw_screen()

    def _handle_input(self, key):
        if key in ('q', 'Q'):
            self.log.debug('die')

            self._sleepy.shutdown()

            raise urwid.ExitMainLoop()

        elif key in ('n', 'N'):
            self._sleepy.next(autoplay=True)

    @property
    def error(self):
        return self._error_text
    
    @error.setter
    def error(self, value):
        self._error_text = value
        self._error.set_text(value)
        self.loop.draw_screen()

    @property
    def artist(self):
        return self.artist_data.get_text()
    
    @artist.setter
    def artist(self, value):
        self.artist_data.set_text(value)

    @property
    def title(self):
        return self.title_data.get_text()
    
    @title.setter
    def title(self, value):
        self.title_data.set_text(value)

    @property
    def album(self):
        return self.album_data.get_text()
    
    @album.setter
    def album(self, value):
        self.album_data.set_text(value)


class WebUI(threading.Thread):
    def __init__(self, sleepy):
        threading.Thread.__init__(self)

        self.log = logging.getLogger(self.__class__.__name__)

        self._sleepy = sleepy
        setattr(flask_app, 'sleepy', sleepy)

        self._server = HTTPServer(WSGIContainer(flask_app))
        self._server.listen(5000)
        self._instance = IOLoop.instance()

        self.start()

    def run(self):
        self._running = True

        tornado.autoreload.start(self._instance)
        self._instance.start()

    def stop(self):
        self._instance.stop()
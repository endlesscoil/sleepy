import logging

from collections import namedtuple

from pandora import Pandora
from cherrymusicclient import CherryMusicClient

class CherryMusicSource(object):
    def __init__(self, url=None):
        self.log = logging.getLogger(self.__class__.__name__)

        self._url = None
        self._cherrymusic = CherryMusicClient()
        self._authenticated = False
        self._current_playlist = None
        self._current_song = None
        self._username = None
        self._password = None
        self._playlists = []

    def authenticate(self):
        self.log.info('Authenticating with CherryMusic..')
        self._authenticated = self._cherrymusic.login(self._username, self._password)
        self.log.debug('Results: %r', self._authenticated)

        if self._authenticated:
            self._cherrymusic.load_playlists()

            self.switch(self._current_playlist)

        return self._authenticated

    def switch(self, playlist_name):
        self.log.info('Switching playlist to %s', playlist_name)
        self._current_playlist = playlist_name

        return self._cherrymusic.select_playlist(playlist_name)

    def next_song(self):
        self.log.info('Retrieving next song..')

        ret = next = None
        if self._cherrymusic.current_playlist:
            next = self._cherrymusic.current_playlist.next_song()
            self._current_song = next

        if next:
            self.log.debug('Next song: %s', next.urlpath)
            ret = '{0}/serve/{1}'.format(self._url, next.urlpath)

        return ret

    def song_info(self):
        self.log.info('Retrieving song info..')
        if self._cherrymusic.current_playlist is None:
            return None

        info = namedtuple('Song', 'artist, album, title')
        info.artist = info.album = info.title = ''

        if self._current_song:
            info.artist = self._current_song.artist
            info.album = self._current_song.album
            info.title = self._current_song.title

        return info

    def add_playlist(self, name):
        self._playlists.append(name)

        if self._current_playlist is None:
            self._current_playlist = name

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value
        self._cherrymusic.url = value

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

class PandoraSource(object):
    def __init__(self, url=None):
        self.log = logging.getLogger(self.__class__.__name__)

        self._pandora = Pandora()
        self._authenticated = False
        self._current_station = None
        self._url = None
        self._username = None
        self._password = None
        self._playlists = []

    def authenticate(self):
        self.log.info('Authenticating with Pandora..')

        self._authenticated = self._pandora.authenticate(self._username, self._password)

        self.log.debug('Results: %r', self._authenticated)

        self.switch(self._current_station)

        return self._authenticated

    def switch(self, station_name):
        self.log.info('Switching playlist to %s', station_name)

        self._current_station = None

        for station in self._pandora.stations:
            if station['stationName'] == station_name:
                self._current_station = station_name
                self._pandora.switch_station(station)

        return self._current_station

    def next_song(self):
        self.log.info('Retrieving next song..')

        self._current_song = self._pandora.get_next_song()

        self.log.debug('Next Song: %s', self._current_song['audioUrlMap']['highQuality']['audioUrl'])

        return self._current_song['audioUrlMap']['highQuality']['audioUrl']

    def song_info(self):
        self.log.info('Retrieving song info..')

        if self._current_song is None:
            return None

        info = namedtuple('Song', 'artist, album, title')
        info.artist = self._current_song['artistName']
        info.album = self._current_song['albumName']
        info.title = self._current_song['songName']

        return info

    def add_playlist(self, name):
        self._playlists.append(name)

        if self._current_station is None:
            self._current_station = name

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value
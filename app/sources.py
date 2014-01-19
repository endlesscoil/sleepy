from collections import namedtuple

from pandora import Pandora
from cherrymusicclient import CherryMusicClient


class CherryMusicSource(object):
    def __init__(self, url=None):
        self._url = None
        self._cherrymusic = CherryMusicClient()
        self._authenticated = False
        self._current_song = None

    def authenticate(self, username, password):
        self._authenticated = self._cherrymusic.login(username, password)

        if self._authenticated:
            self._cherrymusic.load_playlists()

        return self._authenticated

    def switch(self, playlist_name):
        return self._cherrymusic.select_playlist(playlist_name)

    def next_song(self):
        next = None
        if self._cherrymusic.current_playlist:
            next = self._cherrymusic.current_playlist.next_song()
            self._current_song = next

        return '{0}/serve/{1}'.format(self._url, next.urlpath)

    def song_info(self):
        if self._cherrymusic.current_playlist is None:
            return None

        info = namedtuple('Song', 'artist, album, title')
        info.artist = self._current_song.artist
        info.album = self._current_song.album
        info.title = self._current_song.title

        return info

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value
        self._cherrymusic.url = value

class PandoraSource(object):
    def __init__(self, url=None):
        self._pandora = Pandora()
        self._authenticated = False
        self._current_station = None

    def authenticate(self, username, password):
        self._authenticated = self._pandora.authenticate(username, password)

        return self._authenticated

    def switch(self, station_name):
        self._current_station = None

        for station in self._pandora.stations:
            if station['stationName'] == station_name:
                self._current_station = station_name
                self._pandora.switch_station(station)

        return self._current_station

    def next_song(self):
        self._current_song = self._pandora.get_next_song()

        return self._current_song['audioUrlMap']['highQuality']['audioUrl']

    def song_info(self):
        if self._current_song is None:
            return None

        # artistName, albumName, songNAme
        info = namedtuple('Song', 'artist, album, title')
        info.artist = self._current_song['artistName']
        info.album = self._current_song['albumName']
        info.title = self._current_song['songName']

        return info
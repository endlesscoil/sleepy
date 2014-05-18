import logging

from ..db import Source
from .sources import CherryMusicSource, PandoraSource

SOURCES = {
    'cherrymusic': CherryMusicSource,
    'pandora': PandoraSource,
}

class Sources(object):
    def __init__(self, session):
        self.log = logging.getLogger(self.__class__.__name__)
        self._session = session
        self.sources = {}

        self.load()

    def load(self):
        self.log.info('Loading sources from database..')
        sources = self._session.query(Source).all()

        for s in sources:
            self.log.debug('Loading source: %s', s.name)
            source = SOURCES[s.type]()
            source.name = s.name
            source.url = s.url
            source.username = s.username
            source.password = s.password

            for playlist in s.playlists:
                self.log.debug('Adding playlist %s to source %s', playlist.name, s.name)
                source.add_playlist(playlist.name)

            self.sources[s.id] = source

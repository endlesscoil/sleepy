from app.app import Player, Sleepy
from cherrymusicclient.api import api as cmapi
#from pandora import Pandora
from app.sources import PandoraSource, CherryMusicSource


#p = Player()
# source = PandoraSource()

# source.authenticate('', '')
# source.switch('Nuevo Flamenco')

source = CherryMusicSource('http://darkness:8080')
source.authenticate('', '')
source.switch('sleepy')

sleepy = Sleepy(source)

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
sleepy.run()
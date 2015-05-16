from spotify_item import SpotifyItem
from pyechonest import config
from pyechonest import artist
from worker.config import ECHO_NEST_API_KEY


config.ECHO_NEST_API_KEY = ECHO_NEST_API_KEY


class Artist(SpotifyItem):

    def __init__(self, **entries):
        super(Artist, self).__init__(**entries)
        self.echonest = artist.Artist(self.uri)

    def __repr__(self):
        return '<Artist: {0}>'.format(self.name)

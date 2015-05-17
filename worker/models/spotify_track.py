from spotify_item import SpotifyItem
from spotify_album import Album
from spotify_artist import Artist


class Track(SpotifyItem):

    def __init__(self, **entries):
        super(Track, self).__init__(**entries)
        self.album = Album(**self.album)
        self.artists = [Artist(**a) for a in self.artists]

    def __repr__(self):
        return '<Track: {0}>'.format(self.name)

    def export_for_feed(self):
        return {
            'uri': self.uri,
            'name': self.name
        }

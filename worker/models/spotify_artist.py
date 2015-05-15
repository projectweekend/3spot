from spotify_item import SpotifyItem


class Artist(SpotifyItem):

    def __init__(self, **entries):
        super(Artist, self).__init__(**entries)

    def __repr__(self):
        return '<Artist: {0}>'.format(self.name)

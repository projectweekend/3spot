from spotify_item import SpotifyItem


class Album(SpotifyItem):

    def __init__(self, **entries):
        super(Album, self).__init__(**entries)

    def __repr__(self):
        return '<Album: {0}>'.format(self.name)

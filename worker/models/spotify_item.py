import spotipy


class SpotifyItem(object):

    def __init__(self, **entries):
        self.__dict__.update(entries)
        self._client = spotipy.Spotify()

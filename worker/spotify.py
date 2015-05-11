from datetime import datetime
import spotipy


class SpotifyItem(object):

    def __init__(self, **entries):
        self.__dict__.update(entries)
        self._client = spotipy.Spotify()


class Artist(SpotifyItem):

    def __init__(self, **entries):
        super(Artist, self).__init__(**entries)


class Album(SpotifyItem):

    def __init__(self, **entries):
        super(Album, self).__init__(**entries)


class Track(SpotifyItem):

    def __init__(self, **entries):
        super(Track, self).__init__(**entries)
        self.album = Album(**self.album)
        self.artists = [Artist(**a) for a in self.artists]


class PlaylistEntry(SpotifyItem):

    def __init__(self, **entries):
        super(PlaylistEntry, self).__init__(**entries)
        self.track = Track(**self.track)
        self.added_at = datetime.strptime(self.added_at, '%Y-%m-%dT%H:%M:%SZ')
        self.added_date = self.added_at.date()

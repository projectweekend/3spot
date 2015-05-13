from datetime import datetime
import spotipy


class SpotifyItem(object):

    def __init__(self, **entries):
        self.__dict__.update(entries)
        self._client = spotipy.Spotify()


class Artist(SpotifyItem):

    def __init__(self, **entries):
        super(Artist, self).__init__(**entries)

    def __repr__(self):
        return '<Artist: {0}>'.format(self.name)


class Album(SpotifyItem):

    def __init__(self, **entries):
        super(Album, self).__init__(**entries)

    def __repr__(self):
        return '<Album: {0}>'.format(self.name)


class Track(SpotifyItem):

    def __init__(self, **entries):
        super(Track, self).__init__(**entries)
        self.album = Album(**self.album)
        self.artists = [Artist(**a) for a in self.artists]

    def __repr__(self):
        return '<Track: {0}>'.format(self.name)


class Playlist(SpotifyItem):

    def __init__(self, **entries):
        super(Playlist, self).__init__(**entries)
        self.url = self.external_urls['spotify']
        del self.external_urls

    def __repr__(self):
        return '<Playlist: {0}>'.format(self.name)


class PlaylistEntry(SpotifyItem):

    def __init__(self, **entries):
        super(PlaylistEntry, self).__init__(**entries)
        self.track = Track(**self.track)
        self.added_at = datetime.strptime(self.added_at, '%Y-%m-%dT%H:%M:%SZ')
        self.added_date = self.added_at.date()

    def __repr__(self):
        return '<PlaylistEntry: {0}>'.format(self.track.name)

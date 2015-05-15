from datetime import datetime
from spotify_item import SpotifyItem
from spotify_track import Track


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

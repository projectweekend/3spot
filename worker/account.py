from datetime import date
import spotipy
from spotify import PlaylistEntry


class Account(object):

    def __init__(self, username, access_token, refresh_token):
        self._username = username
        self._access_token = access_token
        self._refresh_token = refresh_token
        self._client = spotipy.Spotify(auth=self._access_token)

    def playlist_entries(self, playlist_id):
        offset = 0
        result = self._client.user_playlist_tracks(self._username, playlist_id)
        items = result['items']
        next = result['next']
        while next:
            offset += 50
            result = self._client.user_playlist_tracks(
                user=self._username,
                playlist_id=playlist_id,
                offset=offset)
            items.extend(result['items'])
            next = result['next']
        return [PlaylistEntry(**i) for i in items]

    def todays_track(self, playlist_id):
        def added_today(entry):
            return date.isoformat(date.today()) == date.isoformat(entry.added_date)
        try:
            return filter(added_today, self.playlist_entries(playlist_id))[0]
        except IndexError:
            return None

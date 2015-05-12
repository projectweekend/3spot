from datetime import date
import spotipy
from spotify import Playlist, PlaylistEntry


class Account(object):

    def __init__(self, username, access_token, refresh_token):
        self._username = username
        self._access_token = access_token
        self._refresh_token = refresh_token
        self._client = spotipy.Spotify(auth=self._access_token)

    def playlist(self, playlist_id):
        result = self._client.user_playlist(
            self._username,
            playlist_id,
            fields="name,external_urls")
        return Playlist(**result)

    def todays_track(self, playlist_id):
        def was_added_today(entry):
            return date.isoformat(date.today()) == date.isoformat(entry.added_date)

        offset = 0
        todays_track = None
        while True:
            result = self._client.user_playlist_tracks(
                self._username,
                playlist_id,
                offset=offset)
            entries = [PlaylistEntry(**i) for i in result['items']]
            try:
                todays_track = filter(was_added_today, entries)[0]
                break
            except IndexError:
                if result['next']:
                    offset += 50
                else:
                    break
        return todays_track

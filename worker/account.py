from datetime import date
import spotipy
from boto.dynamodb2.table import Table
from spotify_models import Playlist, PlaylistEntry
from spotify_api import new_access_token


class Account(object):

    def __init__(self, username, playlist_id):
        self._username = username
        self._playlist_id = playlist_id
        self._model = self._database_model()
        self._spotify = self._spotify_client()

    def __repr__(self):
        return "<Account: {0} - {1}>".format(self._username, self._playlist_id)

    def _database_model(self):
        accounts = Table('accounts')
        return accounts.get_item(
            spotify_username=self._username,
            spotify_playlist_id=self._playlist_id)

    def _spotify_client(self):
        self._refresh_access_token()
        return spotipy.Spotify(auth=self._model['access_token'])

    def _refresh_access_token(self):
        self._model['access_token'] = new_access_token(self._model['refresh_token'])
        self._model.save()

    def playlist(self):
        result = self._spotify.user_playlist(
            self._username,
            self._model['spotify_playlist_id'],
            fields="name,external_urls")
        return Playlist(**result)

    def todays_track(self):
        def was_added_today(entry):
            return date.isoformat(date.today()) == date.isoformat(entry.added_date)

        offset = 0
        todays_track = None
        while True:
            result = self._spotify.user_playlist_tracks(
                self._username,
                self._model['spotify_playlist_id'],
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

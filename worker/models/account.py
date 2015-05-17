from datetime import date
from datetime import datetime
import spotipy
from boto.dynamodb2.table import Table
from worker.spotify.api import new_access_token
from spotify_playlist import Playlist, PlaylistEntry


class Account(object):

    def __init__(self, username):
        self._username = username
        self._model = self._database_model()
        self._spotify = self._spotify_client()

    def __repr__(self):
        return "<Account: {0} - {1}>".format(self._username, self._model['spotify_playlist_id'])

    def _database_model(self):
        accounts = Table('accounts')
        return accounts.get_item(
            spotify_username=self._username)

    def _spotify_client(self):
        self._refresh_access_token()
        return spotipy.Spotify(auth=self._model['access_token'])

    def _refresh_access_token(self):
        self._model['access_token'] = new_access_token(self._model['refresh_token'])
        self._model.save()

    def _content_for_feed_item(self, track):
        def artist(a):
            return {
                'uri': a.uri,
                'name': a.name,
                'bio': {
                    'lastfm': a.bio_from_lastfm,
                    'wikipedia': a.bio_from_wikipedia
                },
                'images': a.images,
                'terms': a.popular_terms
            }
        return {
            'track': {
                'uri': track.uri,
                'name': track.name
            },
            'album': {
                'uri': track.album.uri,
                'name': track.album.name,
                'images': track.album.images
            },
            'artists': [artist(a) for a in track.artists]
        }

    def playlist(self):
        result = self._spotify.user_playlist(
            self._username,
            self._model['spotify_playlist_id'],
            fields="name,external_urls")
        return Playlist(**result)

    def todays_playlist_entry(self):
        def was_added_today(item):
            added_at = datetime.strptime(item['added_at'], '%Y-%m-%dT%H:%M:%SZ')
            return date.isoformat(date.today()) == date.isoformat(added_at.date())

        offset = 0
        todays_track = None
        while True:
            result = self._spotify.user_playlist_tracks(
                self._username,
                self._model['spotify_playlist_id'],
                offset=offset)
            try:
                item = filter(was_added_today, result['items'])[0]
                todays_track = PlaylistEntry(**item)
                break
            except IndexError:
                if result['next']:
                    offset += 50
                else:
                    break
        return todays_track

    def add_feed_item(self):
        playlist_entry = self.todays_playlist_entry()
        if playlist_entry:
            date_posted = date.isoformat(playlist_entry.added_date)
            content = self._content_for_feed_item(playlist_entry.track)
            feed_items = Table('feed_items')
            feed_items.put_item(data={
                'spotify_username': self._username,
                'date_posted': date_posted,
                'content': content
            })
            return True
        return False

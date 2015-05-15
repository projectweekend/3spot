import os
import base64
import requests


SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')


def new_access_token(refresh_token):
    auth = base64.b64encode('{0}:{1}'.format(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET))
    headers = {
        'Authorization': 'Basic {0}'.format(auth)
    }
    payload = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }
    response = requests.post(
        'https://accounts.spotify.com/api/token',
        headers=headers,
        data=payload)
    data = response.json()
    return data['access_token']

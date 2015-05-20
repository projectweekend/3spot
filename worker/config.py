import os


SQS_WAIT_TIME = os.getenv('SQS_WAIT_TIME', 20)

SLEEP_TIME = os.getenv('SLEEP_TIME', 60)

PROD_LOGGER = os.getenv('PROD_LOGGER', False)

SQS_QUEUE_NAME = os.getenv('SQS_QUEUE_NAME', 'song-feed-playlists-to-process')

SQS_REGION = os.getenv('SQS_REGION', 'us-east-1')

SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
assert SPOTIFY_CLIENT_ID

SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
assert SPOTIFY_CLIENT_SECRET

ECHO_NEST_API_KEY = os.getenv('ECHO_NEST_API_KEY')
assert ECHO_NEST_API_KEY

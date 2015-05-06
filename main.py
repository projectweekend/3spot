import sys
import getopt
import yaml
import spotipy


def spotify_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


class Spotify(object):

    def __init__(self, username, token, refresh):
        self.username = username
        self.token = token
        self.refresh = refresh
        self.client = self.get_client()

    def get_client(self):
        return spotipy.Spotify(auth=self.token)

    def playlists(self):
        return self.client.user_playlists(self.username)


def main(argv):
    try:
        opts, args = getopt.getopt(argv, 'c')
    except getopt.GetoptError:
        print('Config file missing')
        sys.exit(2)

    config = spotify_config(args[0])

    s = Spotify(config['username'], config['access_token'], config['refresh_token'])
    print(s.playlists())


if __name__ == '__main__':
    main(sys.argv[1:])

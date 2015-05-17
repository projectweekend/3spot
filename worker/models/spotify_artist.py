from spotify_item import SpotifyItem
from pyechonest import config
from pyechonest import artist
from worker.config import ECHO_NEST_API_KEY


config.ECHO_NEST_API_KEY = ECHO_NEST_API_KEY


class Artist(SpotifyItem):

    def __init__(self, **entries):
        super(Artist, self).__init__()
        self.__dict__.update(self._client.artist(entries['uri']))
        self._echonest = artist.Artist(self.uri)
        self.bio_from_lastfm = self._bio_from('last.fm')
        self.bio_from_wikipedia = self._bio_from('wikipedia')
        self.popular_terms = self._popular_terms()

    def __repr__(self):
        return '<Artist: {0}>'.format(self.name)

    def _bio_from(self, site):
        """
        Return Echo Nest biography for artist from the 'site'.
        """
        def belongs_to_site(item):
            return item['site'] == site

        try:
            bio = filter(belongs_to_site, self._echonest.biographies)[0]
        except IndexError:
            return None

        bio_attribution = bio.get('license', {}).get('attribution-url', '')
        bio_text = bio.get('text', '')

        return {
            'attribution': bio_attribution,
            'text': bio_text
        }

    def _popular_terms(self, min_weight=0.45):
        """
        Return Echo Nest terms for artist that have a 'weight' above the 'min_weight'.
        """
        def above_min_weight(item):
            return item['weight'] >= min_weight

        return [p['name'] for p in filter(above_min_weight, self._echonest.terms)]

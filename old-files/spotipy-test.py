'''All of the code needed for Spotipy in the Discord bot.'''
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

SPOTIPY_CLIENT_ID = d['spotify']['clientID']
SPOTIPY_CLIENT_SECRET = d['spotify']['clientSecret']
SPOTIPY_REDIRECT_URI = d['spotify']['redirectURI']

''' Setting Up SpotiPy '''
auth_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
spotify = spotipy.Spotify(auth_manager)

''' Spotipy Methods '''
def list_albums(url):
    results = spotify.artist_albums(url, album_type='album')
    albums = results['items']
    while results['next']:
        results = spotify.next(results)
        albums.extend(results['items'])

    for album in albums:
        print(album['name'])

def find_artist_url(name):
    if len(sys.argv) > 1:
        name = ' '.join(sys.argv[1:])
    else:
        name = 'Radiohead'

    results = spotify.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        artist = items[0]
        print(artist['name'], artist['images'][0]['url'])
        return artist['images'][0]['url']
    else:
        return 'No artist found.'
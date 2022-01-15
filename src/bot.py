''' Import Statements '''
import discord, spotipy
import asyncio, logging
import math, random, re, json, sys
from spotipy.oauth2 import SpotifyClientCredentials


''' Logging '''
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='../logs/discord.log', encoding='utf-8',mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


''' Loading Credentials '''
with open('../pass.json') as f:
    d = json.load(f)

DISCORD = d['discord']

SPOTIPY_CLIENT_ID = d['spotify']['clientID']
SPOTIPY_CLIENT_SECRET = d['spotify']['clientSecret']
SPOTIPY_REDIRECT_URI = d['spotify']['redirectURI']


''' Create Discord Client '''
client = discord.Client()

''' Setting Up SpotiPy '''
auth_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
spotify = spotipy.Spotify(auth_manager)


''' Create General Methods ''' 
def roll(sides):
    tmp = random.randint(0, sides)
    return tmp

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


''' Discord Events '''
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith("roll"):
        print('rolling dice')
        try:
            results = roll(int(message.content.split(' ', 2)[1]))
        except IndexError:
            results = 'Try adding a number of sides after the roll command.'
        await message.channel.send(results)

client.run(DISCORD)

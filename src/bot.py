''' Import Statements '''
import discord, spotipy
import logging, random, json, sys
from discord.ext import commands
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


''' Create Discord Bot '''
description = '''My dog Ruger as a Discord Bot.'''

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='$', description=description, intents=intents)


''' Setting Up SpotiPy '''
auth_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
spotify = spotipy.Spotify(auth_manager)


''' Spotipy Methods '''
# def list_albums(url):
#     results = spotify.artist_albums(url, album_type='album')
#     albums = results['items']
#     while results['next']:
#         results = spotify.next(results)
#         albums.extend(results['items'])

#     for album in albums:
#         print(album['name'])

# def find_artist_url(name):
#     if len(sys.argv) > 1:
#         name = ' '.join(sys.argv[1:])
#     else:
#         name = 'Radiohead'

#     results = spotify.search(q='artist:' + name, type='artist')
#     items = results['artists']['items']
#     if len(items) > 0:
#         artist = items[0]
#         print(artist['name'], artist['images'][0]['url'])
#         return artist['images'][0]['url']
#     else:
#         return 'No artist found.'

''' Discord Bot '''
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def ping(ctx):
    """Adds two numbers together."""
    await ctx.send('pong!')

@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send('{0.name} joined in {0.joined_at}'.format(member))

@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)

@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return
    result = [random.randint(1, limit) for r in range(rolls)]
    results = f'{ctx.author.name} :game_die:\nResults: ' + str(dice) + ' (' + ', '.join(str(i) for i in result) + ')\nTotal: ' + str(sum(result))
    await ctx.send(results)

@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))

bot.run(DISCORD)

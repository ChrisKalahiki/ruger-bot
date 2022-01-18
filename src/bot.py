''' Import Statements '''
import discord, spotipy, nltk
import logging, random, json, sys
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from spotipy.oauth2 import SpotifyClientCredentials


''' Logging - Temporarily disabled '''
# logger = logging.getLogger('discord')
# logger.setLevel(logging.DEBUG)
# handler = logging.FileHandler(filename='../logs/discord.log', encoding='utf-8',mode='w')
# handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
# logger.addHandler(handler)


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

bot = commands.Bot(command_prefix='.', description=description, intents=intents)
slash = SlashCommand(bot, override_type = True)


''' Setting Up SpotiPy '''
auth_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
spotify = spotipy.Spotify(auth_manager)


''' Discord Bot '''
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@slash.slash(name="test")
async def _test(ctx: SlashContext):
    await ctx.send("Hello World!")

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

bot.load_extension("cog")

bot.run(DISCORD)

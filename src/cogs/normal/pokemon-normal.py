import json
import os
import platform
import random
import sys

import aiohttp
import disnake
from disnake.ext import commands
from disnake.ext.commands import Context

from helpers import checks
import logging

if not os.path.isfile("../config.json"):
    sys.exit("'config.json' not found by general-normal! Please add it and try again.")
else:
    with open("../config.json") as file:
        config = json.load(file)

if not os.path.isfile("../data/players.json"):
    sys.exit("'players.json' not found by pokemon-normal! Please add it and try again.")
else:
    with open("../data/players.json") as file:
        players = json.load(file)

if not os.path.isfile("../data/rankings.json"):
    sys.exit("'rankings.json' not found by pokemon-normal! Please add it and try again.")
else:
    with open("../data/rankings.json") as file:
        rank = json.load(file)

''' Logging '''
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='../logs/discord.log', encoding='utf-8',mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

class Pokemon(commands.Cog, name='pokemon-normal'):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(
        name='register',
        description='Register to the Pokemon ranking system.'
    )
    @checks.not_blacklisted()
    async def register(self, ctx: Context):
        if ctx.author.id in players:
            await ctx.send('You are already registered!')
        else:
            players[ctx.author.id] = {
                'name': ctx.author.name,
                'rank': 0,
                'xp': 0,
                'level': 1,
                'badges': {
                    'gold': 0,
                    'silver': 0,
                    'bronze': 0
                }
            }
            await ctx.send('You have been registered!')
            with open('../data/players.json', 'w') as file:
                json.dump(players, file, indent=4)
    
    @commands.command(
        name='unregister',
        description='Unregister from the Pokemon ranking system.'
    )
    @checks.not_blacklisted()
    async def unregister(self, ctx: Context):
        if ctx.author.id in players:
            del players[ctx.author.id]
            await ctx.send('You have been unregistered!')
            with open('../data/players.json', 'w') as file:
                json.dump(players, file, indent=4)
        else:
            await ctx.send('You are not registered!')
    
    @commands.command(
        name='rank',
        description='Check your rank.'
    )
    @checks.not_blacklisted()
    async def rank(self, ctx: Context):
        if ctx.author.id in players:
            await ctx.send(f'You are ranked #{players[ctx.author.id]["rank"]} with {players[ctx.author.id]["xp"]} XP!')
        else:
            await ctx.send('You are not registered!')
    
    @commands.command(
        name='badges',
        description='Check your badges.'
    )
    @checks.not_blacklisted()
    async def badges(self, ctx: Context):
        if ctx.author.id in players:
            await c


def setup(bot):
    bot.add_cog(General(bot))
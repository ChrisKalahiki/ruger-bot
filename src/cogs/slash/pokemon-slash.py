import json
import os
import platform
import random
import sys

import aiohttp
import disnake
from disnake import ApplicationCommandInteraction, Option, OptionType
from disnake.ext import commands

from helpers import checks
import logging

if not os.path.isfile("../config.json"):
    sys.exit("'config.json' not found by pokemon-slash! Please add it and try again.")
else:
    with open("../config.json") as file:
        config = json.load(file)

if not os.path.isfile("../data/players.json"):
    sys.exit("'players.json' not found by pokemon-slash! Please add it and try again.")
else:
    with open("../data/players.json") as file:
        players = json.load(file)

if not os.path.isfile("../data/rankings.json"):
    sys.exit("'rankings.json' not found by pokemon-slash! Please add it and try again.")
else:
    with open("../data/rankings.json") as file:
        rank = json.load(file)

''' Logging '''
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='../logs/discord.log', encoding='utf-8',mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

class Pokemon(commands.Cog, name='pokemon-slash'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='register',
        description='Register to the Pokemon ranking system.'
    )
    @checks.not_blacklisted()
    async def register(self, interaction: ApplicationCommandInteraction):
        if interaction.author.id in players:
            await interaction.send('You are already registered!')
        else:
            players[interaction.author.id] = {
                'name': interaction.author.name,
                'rank': 0,
                'xp': 0,
                'level': 1,
                'badges': {
                    'gold': 0,
                    'silver': 0,
                    'bronze': 0
                }
            }
            await interaction.send('You have been registered!')
            with open('../data/players.json', 'w') as file:
                json.dump(players, file, indent=4)
    
    @commands.command(
        name='unregister',
        description='Unregister from the Pokemon ranking system.'
    )
    @checks.not_blacklisted()
    async def unregister(self, interaction: ApplicationCommandInteraction):
        if interaction.author.id in players:
            del players[interaction.author.id]
            await interaction.send('You have been unregistered!')
            with open('../data/players.json', 'w') as file:
                json.dump(players, file, indent=4)
        else:
            await interaction.send('You are not registered!')
    
    @commands.command(
        name='rank',
        description='Check your rank.'
    )
    @checks.not_blacklisted()
    async def rank(self, interaction: ApplicationCommandInteraction):
        if interaction.author.id in players:
            await interaction.send(f'You are ranked #{players[interaction.author.id]["rank"]} with {players[interaction.author.id]["xp"]} XP!')
        else:
            await interaction.send('You are not registered!')
    
    @commands.command(
        name='badges',
        description='Check your badges.'
    )
    @checks.not_blacklisted()
    async def badges(self, interaction: ApplicationCommandInteraction):
        if interaction.author.id in players:
            await c



def setup(bot):
    bot.add_cog(General(bot))
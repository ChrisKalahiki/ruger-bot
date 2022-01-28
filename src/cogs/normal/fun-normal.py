import json
import os
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

''' Logging '''
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='../logs/discord.log', encoding='utf-8',mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


class Choice(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.choice = None

    @disnake.ui.button(label="Heads", style=disnake.ButtonStyle.blurple)
    async def confirm(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.choice = button.label.lower()
        self.stop()

    @disnake.ui.button(label="Tails", style=disnake.ButtonStyle.blurple)
    async def cancel(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.choice = button.label.lower()
        self.stop()


class RockPaperScissors(disnake.ui.Select):
    def __init__(self):

        options = [
            disnake.SelectOption(
                label="Scissors", description="You choose scissors.", emoji="🪨"
            ),
            disnake.SelectOption(
                label="Rock", description="You choose rock.", emoji="🧻"
            ),
            disnake.SelectOption(
                label="paper", description="You choose paper.", emoji="✂"
            ),
        ]

        super().__init__(
            placeholder="Choose...",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: disnake.MessageInteraction):
        choices = {
            "rock": 0,
            "paper": 1,
            "scissors": 2,
        }
        user_choice = self.values[0].lower()
        user_choice_index = choices[user_choice]

        bot_choice = random.choice(list(choices.keys()))
        bot_choice_index = choices[bot_choice]

        result_embed = disnake.Embed(color=0x9C84EF)
        result_embed.set_author(name=interaction.author.display_name, icon_url=interaction.author.avatar.url)

        if user_choice_index == bot_choice_index:
            result_embed.description = f"**That's a draw!**\nYou've chosen {user_choice} and I've chosen {bot_choice}."
            result_embed.colour = 0xF59E42
        elif user_choice_index == 0 and bot_choice_index == 2:
            result_embed.description = f"**You won!**\nYou've chosen {user_choice} and I've chosen {bot_choice}."
            result_embed.colour = 0x9C84EF
        elif user_choice_index == 1 and bot_choice_index == 0:
            result_embed.description = f"**You won!**\nYou've chosen {user_choice} and I've chosen {bot_choice}."
            result_embed.colour = 0x9C84EF
        elif user_choice_index == 2 and bot_choice_index == 1:
            result_embed.description = f"**You won!**\nYou've chosen {user_choice} and I've chosen {bot_choice}."
            result_embed.colour = 0x9C84EF
        else:
            result_embed.description = f"**I won!**\nYou've chosen {user_choice} and I've chosen {bot_choice}."
            result_embed.colour = 0xE02B2B
        await interaction.response.defer()
        await interaction.edit_original_message(embed=result_embed, content=None, view=None)


class RockPaperScissorsView(disnake.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(RockPaperScissors())


class Fun(commands.Cog, name="fun-normal"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="randomfact",
        description="Get a random fact."
    )
    @checks.not_blacklisted()
    async def randomfact(self, context: Context):
        """
        Get a random fact.
        :param context: The context in which the command has been executed.
        """
        # This will prevent your bot from stopping everything when doing a web request - see: https://discordpy.readthedocs.io/en/stable/faq.html#how-do-i-make-a-web-request
        async with aiohttp.ClientSession() as session:
            async with session.get("https://uselessfacts.jsph.pl/random.json?language=en") as request:
                if request.status == 200:
                    data = await request.json()
                    embed = disnake.Embed(
                        description=data["text"],
                        color=0xD75BF4
                    )
                else:
                    embed = disnake.Embed(
                        title="Error!",
                        description="There is something wrong with the API, please try again later",
                        color=0xE02B2B
                    )
                logger.info(f"{context.author} used the 'randomfact' command.")
                await context.send(embed=embed)

    @commands.command(
        name="coinflip",
        description="Make a coin flip, but give your bet before."
    )
    @checks.not_blacklisted()
    async def coinflip(self, context: Context) -> None:
        """
        Make a coin flip, but give your bet before.
        :param context: The context in which the command has been executed.
        """
        buttons = Choice()
        embed = disnake.Embed(
            description="What is your bet?",
            color=0x9C84EF
        )
        message = await context.send(embed=embed, view=buttons)
        await buttons.wait()  # We wait for the user to click a button.
        result = random.choice(["heads", "tails"])
        if buttons.choice == result:
            # User guessed correctly
            embed = disnake.Embed(
                description=f"Correct! You guessed `{buttons.choice}` and I flipped the coin to `{result}`.",
                color=0x9C84EF
            )
        else:
            embed = disnake.Embed(
                description=f"Woops! You guessed `{buttons.choice}` and I flipped the coin to `{result}`, better luck next time!",
                color=0xE02B2B
            )
        logger.info(f"{context.author} used the 'coinflip' command.")
        await message.edit(embed=embed, view=None)

    @commands.command(
        name="rps",
        description="Play the rock paper scissors against the bot."
    )
    @checks.not_blacklisted()
    async def rock_paper_scissors(self, context: Context) -> None:
        """
        Play the rock paper scissors game against the bot.
        :param context: The context in which the command has been executed.
        """
        view = RockPaperScissorsView()
        logger.info(f"{context.author} used the 'rps' command.")
        await context.send("Please make your choice", view=view)

    @commands.command(
        name="mtg",
        description="Search for a card in MTG."
    )
    @checks.not_blacklisted()
    async def mtg(self, context: Context, *, query: str) -> None:
        """
        Search for a card in MTG.
        :param context: The context in which the command has been executed.
        :param query: The query to search for.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.scryfall.com/cards/named?fuzzy={query}") as request:
                if request.status == 200:
                    data = await request.json()
                    description = ""
                    if data['set_name'] != None: description = description + f"Set: {data['set_name']}"
                    if data['prices']['usd'] != None: description = description + f"\nPrice: ${data['prices']['usd']}"
                    embed = disnake.Embed(
                        title=data["name"],
                        description=description,
                        url=data["scryfall_uri"],
                        color=0x9C84EF
                    )
                    embed.set_image(url=data["image_uris"]["normal"])
                else:
                    embed = disnake.Embed(
                        title="Error!",
                        description="There is something wrong with the API, please try again later",
                        color=0xE02B2B
                    )
                logger.info(f"{context.author} used the 'mtg' command to search for {query}.")
                await context.send(embed=embed)

    @commands.command(
        name="pokemon",
        description="Search for a pokemon."
    )
    @checks.not_blacklisted()
    async def pokemon(self, context: Context, *, query: str) -> None:
        """
        Search for a pokemon.
        :param context: The context in which the command has been executed.
        :param query: The query to search for.
        """
        async with aiohttp.ClientSession() as session:
            query = query.lower()
            async with session.get(f"https://pokeapi.co/api/v2/pokemon/{query}") as request:
                if request.status == 200:
                    data = await request.json()
                    embed = disnake.Embed(
                        title=data["name"],
                        description=data["types"][0]["type"]["name"],
                        color=0x9C84EF
                    )
                    embed.set_image(url=data["sprites"]["front_default"])
                else:
                    embed = disnake.Embed(
                        title="Error!",
                        description="There is something wrong with the API, please try again later",
                        color=0xE02B2B
                    )
                logger.info(f"{context.author} used the 'pokemon' command to search for {query}.")
                await context.send(embed=embed)

    @commands.command(
        name="anime",
        description="Search for an anime."
    )
    @checks.not_blacklisted()
    async def anime(self, context: Context, *, query: str) -> None:
        """
        Search for an anime.
        :param context: The context in which the command has been executed.
        :param query: The query to search for.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.jikan.moe/v3/search/anime?q={query}") as request:
                if request.status == 200:
                    data = await request.json()
                    embed = disnake.Embed(
                        title=data["results"][0]["title"],
                        description=data["results"][0]["synopsis"],
                        color=0x9C84EF
                    )
                    embed.set_image(url=data["results"][0]["image_url"])
                else:
                    embed = disnake.Embed(
                        title="Error!",
                        description="There is something wrong with the API, please try again later",
                        color=0xE02B2B
                    )
                logger.info(f"{context.author} used the 'anime' command to search for {query}.")
                await context.send(embed=embed)

    @commands.command(
        name="manga",
        description="Search for a manga."
    )
    @checks.not_blacklisted()
    async def manga(self, context: Context, *, query: str) -> None:
        """
        Search for a manga.
        :param context: The context in which the command has been executed.
        :param query: The query to search for.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.jikan.moe/v3/search/manga?q={query}") as request:
                if request.status == 200:
                    data = await request.json()
                    embed = disnake.Embed(
                        title=data["results"][0]["title"],
                        description=data["results"][0]["synopsis"],
                        color=0x9C84EF
                    )
                    embed.set_image(url=data["results"][0]["image_url"])
                else:
                    embed = disnake.Embed(
                        title="Error!",
                        description="There is something wrong with the API, please try again later",
                        color=0xE02B2B
                    )
                logger.info(f"{context.author} used the 'manga' command to search for {query}.")
                await context.send(embed=embed)

def setup(bot):
    bot.add_cog(Fun(bot))
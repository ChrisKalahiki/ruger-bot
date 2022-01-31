import json
import os
import sys

import disnake
from disnake.ext import commands
from disnake.ext.commands import Context

from helpers import json_manager, checks
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

class Owner(commands.Cog, name="owner-normal"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="shutdown",
        description="Make the bot shutdown.",
    )
    @checks.is_owner()
    async def shutdown(self, context: Context):
        """
        Makes the bot shutdown.
        """
        embed = disnake.Embed(
            description="Shutting down. Bye! :wave:",
            color=0x9C84EF
        )
        logger.info(f"Shutting down. Bye! :wave:")
        await context.send(embed=embed)
        await self.bot.close()

    @commands.command(
        name="say",
        description="The bot will say anything you want.",
    )
    @checks.is_owner()
    async def say(self, context: Context, *, message: str):
        """
        The bot will say anything you want.
        """
        logger.info(f"Saying '{message}'")
        await context.send(message)

    @commands.command(
        name="embed",
        description="The bot will say anything you want, but within embeds.",
    )
    @checks.is_owner()
    async def embed(self, context: Context, *, message: str):
        """
        The bot will say anything you want, but within embeds.
        """
        embed = disnake.Embed(
            description=message,
            color=0x9C84EF
        )
        logger.info(f"Saying '{message}'")
        await context.send(embed=embed)

    @commands.group(
        name="blacklist"
    )
    async def blacklist(self, context: Context):
        """
        Lets you add or remove a user from not being able to use the bot.
        """
        if context.invoked_subcommand is None:
            with open("../data/blacklist.json") as file:
                blacklist = json.load(file)
            embed = disnake.Embed(
                title=f"There are currently {len(blacklist['ids'])} blacklisted IDs",
                description=f"{', '.join(str(id) for id in blacklist['ids'])}",
                color=0x9C84EF
            )
            await context.send(embed=embed)

    @blacklist.command(
        name="add"
    )
    async def blacklist_add(self, context: Context, member: disnake.Member = None):
        """
        Lets you add a user from not being able to use the bot.
        """
        try:
            user_id = member.id
            with open("../data/blacklist.json") as file:
                blacklist = json.load(file)
            if user_id in blacklist['ids']:
                embed = disnake.Embed(
                    title="Error!",
                    description=f"**{member.name}** is already in the blacklist.",
                    color=0xE02B2B
                )
                return await context.send(embed=embed)
            json_manager.add_user_to_blacklist(user_id)
            embed = disnake.Embed(
                title="User Blacklisted",
                description=f"**{member.name}** has been successfully added to the blacklist",
                color=0x9C84EF
            )
            with open("../data/blacklist.json") as file:
                blacklist = json.load(file)
            embed.set_footer(
                text=f"There are now {len(blacklist['ids'])} users in the blacklist"
            )
            logger.info(f"{member.name} has been added to the blacklist.")
            await context.send(embed=embed)
        except:
            embed = disnake.Embed(
                title="Error!",
                description=f"An unknown error occurred when trying to add **{member.name}** to the blacklist.",
                color=0xE02B2B
            )
            await context.send(embed=embed)

    @blacklist.command(
        name="remove"
    )
    async def blacklist_remove(self, context, member: disnake.Member = None):
        """
        Lets you remove a user from not being able to use the bot.
        """
        try:
            user_id = member.id
            json_manager.remove_user_from_blacklist(user_id)
            embed = disnake.Embed(
                title="User removed from blacklist",
                description=f"**{member.name}** has been successfully removed from the blacklist",
                color=0x9C84EF
            )
            with open("../data/blacklist.json") as file:
                blacklist = json.load(file)
            embed.set_footer(
                text=f"There are now {len(blacklist['ids'])} users in the blacklist"
            )
            logger.info(f"{member.name} has been removed from the blacklist.")
            await context.send(embed=embed)
        except:
            embed = disnake.Embed(
                title="Error!",
                description=f"**{member.name}** is not in the blacklist.",
                color=0xE02B2B
            )
            await context.send(embed=embed)


def setup(bot):
    bot.add_cog(Owner(bot))
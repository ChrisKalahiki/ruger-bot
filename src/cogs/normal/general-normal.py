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

''' Logging '''
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='../logs/discord.log', encoding='utf-8',mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


class General(commands.Cog, name="general-normal"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="botinfo",
        description="Get some useful (or not) information about the bot.",
    )
    @checks.not_blacklisted()
    async def botinfo(self, context: Context) -> None:
        """
        Get some useful (or not) information about the bot.
        :param context: The context in which the command has been executed.
        """
        embed = disnake.Embed(
            description="The Ruger Discord Bot.",
            color=0x9C84EF
        )
        embed.set_author(
            name="Bot Information"
        )
        embed.add_field(
            name="Owner:",
            value="Kalafreaky#0808",
            inline=True
        )
        embed.add_field(
            name="Python Version:",
            value=f"{platform.python_version()}",
            inline=True
        )
        embed.add_field(
            name="Prefix:",
            value=f"/ (Slash Commands) or {config['prefix']} for normal commands",
            inline=False
        )
        embed.set_footer(
            text=f"Requested by {context.author}"
        )
        logger.info(f"Bot info requested by {context.author}.")
        await context.send(embed=embed)

    @commands.command(
        name="serverinfo",
        description="Get some useful (or not) information about the server.",
    )
    @checks.not_blacklisted()
    async def serverinfo(self, context: Context) -> None:
        """
        Get some useful (or not) information about the server.
        :param context: The context in which the command has been executed.
        """
        roles = [role.name for role in context.guild.roles]
        if len(roles) > 50:
            roles = roles[:50]
            roles.append(f">>>> Displaying[50/{len(roles)}] Roles")
        roles = ", ".join(roles)

        embed = disnake.Embed(
            title="**Server Name:**",
            description=f"{context.guild}",
            color=0x9C84EF
        )
        embed.set_thumbnail(
            url=context.guild.icon.url
        )
        embed.add_field(
            name="Server ID",
            value=context.guild.id
        )
        embed.add_field(
            name="Member Count",
            value=context.guild.member_count
        )
        embed.add_field(
            name="Text/Voice Channels",
            value=f"{len(context.guild.channels)}"
        )
        embed.add_field(
            name=f"Roles ({len(context.guild.roles)})",
            value=roles
        )
        embed.set_footer(
            text=f"Created at: {context.guild.created_at}"
        )
        logger.info(f"Server info requested by {context.author}.")
        await context.send(embed=embed)

    @commands.command(
        name="ping",
        description="Check if the bot is alive.",
    )
    @checks.not_blacklisted()
    async def ping(self, context: Context) -> None:
        """
        Check if the bot is alive.
        :param context: The context in which the command has been executed.
        """
        embed = disnake.Embed(
            title="🏓 Pong!",
            description=f"The bot latency is {round(self.bot.latency * 1000)}ms.",
            color=0x9C84EF
        )
        logger.info(f"{context.author} pinged the bot.")
        await context.send(embed=embed)

    @commands.command(
        name="joined",
        description="See when a member joined.",
    )
    @checks.not_blacklisted()
    async def joined(self, context: Context, member: disnake.Member) -> None:
        """
        See when a member joined.
        :param context: The context in which the command has been executed.
        :param member: The member to check.
        """
        embed = disnake.Embed(
            title="Member Joined",
            description='{0.name} joined in {0.joined_at}'.format(member),
            color=0x9C84EF
        )
        logger.info(f"{context.author} requested the join date of {member}.")
        await context.send(embed=embed)

    @commands.command(
        name="choose",
        description="Let the bot choose for you.",
    )
    @checks.not_blacklisted()
    async def choose(self, context: Context, *choices: str) -> None:
        """
        Let the bot choose for you.
        :param context: The context in which the command has been executed.
        :param choices: The choices to choose from.
        """
        embed = disnake.Embed(
            title="The bot has chosen:",
            description=f"{random.choice(choices)}",
            color=0x9C84EF
        )
        logger.info(f"{context.author} chose from {choices}.")
        await context.send(embed=embed)

    @commands.command(
        name="roll",
        description="Roll NdN dice.",
    )
    @checks.not_blacklisted()
    async def roll(self, context: Context, dice: str) -> None:
        """
        Roll NdN dice.
        :param context: The context in which the command has been executed.
        :param dice: The number of dice to roll.
        """
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await context.send('Format has to be in NdN!')
            return
        result = [random.randint(1, limit) for r in range(rolls)]
        embed = disnake.Embed(
            title=f"{context.author.name} :game_die:",
            description=f'Results: ' + str(dice) + ' (' + ', '.join(str(i) for i in result) + ')\nTotal: ' + str(sum(result)),
            color=0x9C84EF
        )
        logger.info(f"{context.author} rolled {dice}.")
        await context.send(embed=embed)

    # @commands.command(
    #     name="invite",
    #     description="Get the invite link of the bot to be able to invite it.",
    # )
    # @checks.not_blacklisted()
    # async def invite(self, context: Context) -> None:
    #     """
    #     Get the invite link of the bot to be able to invite it.
    #     :param context: The context in which the command has been executed.
    #     """
    #     embed = disnake.Embed(
    #         description=f"Invite me by clicking [here](https://discordapp.com/oauth2/authorize?&client_id={config['application_id']}&scope=bot+applications.commands&permissions={config['permissions']}).",
    #         color=0xD75BF4
    #     )
    #     try:
    #         # To know what permissions to give to your bot, please see here: https://discordapi.com/permissions.html and remember to not give Administrator permissions.
    #         await context.author.send(embed=embed)
    #         await context.send("I sent you a private message!")
    #     except disnake.Forbidden:
    #         await context.send(embed=embed)

    # @commands.command(
    #     name="server",
    #     description="Get the invite link of the discord server of the bot for some support.",
    # )
    # @checks.not_blacklisted()
    # async def server(self, context: Context) -> None:
    #     """
    #     Get the invite link of the discord server of the bot for some support.
    #     :param context: The context in which the command has been executed.
    #     """
    #     embed = disnake.Embed(
    #         description=f"Join the support server for the bot by clicking [here](https://discord.gg/mTBrXyWxAF).",
    #         color=0xD75BF4
    #     )
    #     try:
    #         await context.author.send(embed=embed)
    #         await context.send("I sent you a private message!")
    #     except disnake.Forbidden:
    #         await context.send(embed=embed)

    @commands.command(
        name="8ball",
        description="Ask any question to the bot.",
    )
    @checks.not_blacklisted()
    async def eight_ball(self, context: Context, *, question: str) -> None:
        """
        Ask any question to the bot.
        :param context: The context in which the command has been executed.
        :param question: The question that should be asked by the user.
        """
        answers = ["It is certain.", "It is decidedly so.", "You may rely on it.", "Without a doubt.",
                   "Yes - definitely.", "As I see, yes.", "Most likely.", "Outlook good.", "Yes.",
                   "Signs point to yes.", "Reply hazy, try again.", "Ask again later.", "Better not tell you now.",
                   "Cannot predict now.", "Concentrate and ask again later.", "Don't count on it.", "My reply is no.",
                   "My sources say no.", "Outlook not so good.", "Very doubtful."]
        embed = disnake.Embed(
            title="**My Answer:**",
            description=f"{random.choice(answers)}",
            color=0x9C84EF
        )
        embed.set_footer(
            text=f"The question was: {question}"
        )
        logger.info(f"{context.author} asked the bot a question: {question}.")
        await context.send(embed=embed)

    @commands.command(
        name="bitcoin",
        description="Get the current price of bitcoin.",
    )
    @checks.not_blacklisted()
    async def bitcoin(self, context: Context) -> None:
        """
        Get the current price of bitcoin.
        :param context: The context in which the command has been executed.
        """
        # This will prevent your bot from stopping everything when doing a web request - see: https://discordpy.readthedocs.io/en/stable/faq.html#how-do-i-make-a-web-request
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.coindesk.com/v1/bpi/currentprice/BTC.json") as request:
                if request.status == 200:
                    data = await request.json(
                        content_type="application/javascript")  # For some reason the returned content is of type JavaScript
                    embed = disnake.Embed(
                        title="Bitcoin price",
                        description=f"The current price is {data['bpi']['USD']['rate']} :dollar:",
                        color=0x9C84EF
                    )
                else:
                    embed = disnake.Embed(
                        title="Error!",
                        description="There is something wrong with the API, please try again later",
                        color=0xE02B2B
                    )
                logger.info(f"{context.author} asked the bot for the current price of bitcoin.")
                await context.send(embed=embed)


def setup(bot):
    bot.add_cog(General(bot))
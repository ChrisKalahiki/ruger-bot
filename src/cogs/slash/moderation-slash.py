import json
import os
import sys

import disnake
from disnake import ApplicationCommandInteraction, Option, OptionType
from disnake.ext import commands

from helpers import checks
import logging

if not os.path.isfile("../config.json"):
    sys.exit("'config.json' not found by general-normal! Please add it and try again.")
else:
    with open("../config.json") as file:
        config = json.load(file)

''' Logging '''
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='../logs/discord.log', encoding='utf-8',mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


class Moderation(commands.Cog, name="moderation-slash"):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="kick",
        description="Kick a user out of the server.",
        options=[
            Option(
                name="user",
                description="The user you want to kick.",
                type=OptionType.user,
                required=True
            ),
            Option(
                name="reason",
                description="The reason you kicked the user.",
                type=OptionType.string,
                required=False
            )
        ]
    )
    @commands.has_permissions(kick_members=True)
    @checks.not_blacklisted()
    async def kick(self, interaction: ApplicationCommandInteraction, user: disnake.User,
                   reason: str = "Not specified") -> None:
        """
        Kick a user out of the server.
        :param interaction: The application command interaction.
        :param user: The user that should be kicked from the server.
        :param reason: The reason for the kick. Default is "Not specified".
        """
        member = await interaction.guild.get_or_fetch_member(user.id)
        if member.guild_permissions.administrator:
            embed = disnake.Embed(
                title="Error!",
                description="User has Admin permissions.",
                color=0xE02B2B
            )
            await interaction.send(embed=embed)
        else:
            try:
                embed = disnake.Embed(
                    title="User Kicked!",
                    description=f"**{member}** was kicked by **{interaction.author}**!",
                    color=0x9C84EF
                )
                embed.add_field(
                    name="Reason:",
                    value=reason
                )
                logging.info(f"{member} was kicked by {interaction.author} for {reason}!")
                await interaction.send(embed=embed)
                try:
                    await member.send(
                        f"You were kicked by **{interaction.author}**!\nReason: {reason}"
                    )
                except disnake.Forbidden:
                    # Couldn't send a message in the private messages of the user
                    pass
                await member.kick(reason=reason)
            except:
                embed = disnake.Embed(
                    title="Error!",
                    description="An error occurred while trying to kick the user. Make sure my role is above the role of the user you want to kick.",
                    color=0xE02B2B
                )
                await interaction.send(embed=embed)

    @commands.slash_command(
        name="nick",
        description="Change the nickname of a user on a server.",
        options=[
            Option(
                name="user",
                description="The user you want to change the nickname.",
                type=OptionType.user,
                required=True
            ),
            Option(
                name="nickname",
                description="The new nickname of the user.",
                type=OptionType.string,
                required=False
            )
        ],
    )
    @commands.has_permissions(manage_nicknames=True)
    @checks.not_blacklisted()
    async def nick(self, interaction: ApplicationCommandInteraction, user: disnake.User, nickname: str = None) -> None:
        """
        Change the nickname of a user on a server.
        :param interaction: The application command interaction.
        :param user: The user that should have its nickname changed.
        :param nickname: The new nickname of the user. Default is None, which will reset the nickname.
        """
        member = await interaction.guild.get_or_fetch_member(user.id)
        try:
            await member.edit(nick=nickname)
            embed = disnake.Embed(
                title="Changed Nickname!",
                description=f"**{member}'s** new nickname is **{nickname}**!",
                color=0x9C84EF
            )
            logging.info(f"{member}'s new nickname is {nickname} by {interaction.author}!")
            await interaction.send(embed=embed)
        except:
            embed = disnake.Embed(
                title="Error!",
                description="An error occurred while trying to change the nickname of the user. Make sure my role is above the role of the user you want to change the nickname.",
                color=0xE02B2B
            )
            await interaction.send(embed=embed)

    @commands.slash_command(
        name="ban",
        description="Bans a user from the server.",
        options=[
            Option(
                name="user",
                description="The user you want to ban.",
                type=OptionType.user,
                required=True
            ),
            Option(
                name="reason",
                description="The reason you banned the user.",
                type=OptionType.string,
                required=False
            )
        ],
    )
    @commands.has_permissions(ban_members=True)
    @checks.not_blacklisted()
    async def ban(self, interaction: ApplicationCommandInteraction, user: disnake.User,
                  reason: str = "Not specified") -> None:
        """
        Bans a user from the server.
        :param interaction: The application command interaction.
        :param user: The user that should be banned from the server.
        :param reason: The reason for the ban. Default is "Not specified".
        """
        member = await interaction.guild.get_or_fetch_member(user.id)
        try:
            if member.guild_permissions.administrator:
                embed = disnake.Embed(
                    title="Error!",
                    description="User has Admin permissions.",
                    color=0xE02B2B
                )
                await interaction.send(embed=embed)
            else:
                embed = disnake.Embed(
                    title="User Banned!",
                    description=f"**{member}** was banned by **{interaction.author}**!",
                    color=0x9C84EF
                )
                embed.add_field(
                    name="Reason:",
                    value=reason
                )
                logging.info(f"{member} was banned by {interaction.author} for {reason}!")
                await interaction.send(embed=embed)
                try:
                    await member.send(f"You were banned by **{interaction.author}**!\nReason: {reason}")
                except disnake.Forbidden:
                    # Couldn't send a message in the private messages of the user
                    pass
                await member.ban(reason=reason)
        except:
            embed = disnake.Embed(
                title="Error!",
                description="An error occurred while trying to ban the user. Make sure my role is above the role of the user you want to ban.",
                color=0xE02B2B
            )
            await interaction.send(embed=embed)

    @commands.slash_command(
        name="warn",
        description="Warns a user in the server.",
        options=[
            Option(
                name="user",
                description="The user you want to warn.",
                type=OptionType.user,
                required=True
            ),
            Option(
                name="reason",
                description="The reason you warned the user.",
                type=OptionType.string,
                required=False
            )
        ],
    )
    @commands.has_permissions(manage_messages=True)
    @checks.not_blacklisted()
    async def warn(self, interaction: ApplicationCommandInteraction, user: disnake.User,
                   reason: str = "Not specified") -> None:
        """
        Warns a user in his private messages.
        :param interaction: The application command interaction.
        :param user: The user that should be warned.
        :param reason: The reason for the warn. Default is "Not specified".
        """
        member = await interaction.guild.get_or_fetch_member(user.id)
        embed = disnake.Embed(
            title="User Warned!",
            description=f"**{member}** was warned by **{interaction.author}**!",
            color=0x9C84EF
        )
        embed.add_field(
            name="Reason:",
            value=reason
        )
        logging.info(f"{member} was warned by {interaction.author} for {reason}!")
        await interaction.send(embed=embed)
        try:
            await member.send(f"You were warned by **{interaction.author}**!\nReason: {reason}")
        except disnake.Forbidden:
            # Couldn't send a message in the private messages of the user
            await interaction.send(f"{member.mention}, you were warned by **{interaction.author}**!\nReason: {reason}")

    @commands.slash_command(
        name="purge",
        description="Delete a number of messages.",
        options=[
            Option(
                name="amount",
                description="The amount of messages you want to delete. (Must be between 1 and 100.)",
                type=OptionType.integer,
                required=True,
                min_value=1,
                max_value=100
            )
        ],
    )
    @commands.has_guild_permissions(manage_messages=True)
    @checks.not_blacklisted()
    async def purge(self, interaction: ApplicationCommandInteraction, amount: int) -> None:
        """
        Delete a number of messages.
        :param interaction: The application command interaction.
        :param amount: The number of messages that should be deleted.
        """
        purged_messages = await interaction.channel.purge(limit=amount)
        embed = disnake.Embed(
            title="Chat Cleared!",
            description=f"**{interaction.author}** cleared **{len(purged_messages)}** messages!",
            color=0x9C84EF
        )
        logging.info(f"{interaction.author} cleared {len(purged_messages)} messages!")
        await interaction.send(embed=embed)

    @commands.slash_command(
        name="hackban",
        description="Bans a user without the user having to be in the server.",
        options=[
            Option(
                name="user_id",
                description="The ID of the user that should be banned.",
                type=OptionType.string,
                required=True
            ),
            Option(
                name="reason",
                description="The reason you banned the user.",
                type=OptionType.string,
                required=False
            )
        ]
    )
    @commands.has_permissions(ban_members=True)
    @checks.not_blacklisted()
    async def hackban(self, interaction: ApplicationCommandInteraction, user_id: str,
                      reason: str = "Not specified") -> None:
        """
        Bans a user without the user having to be in the server.
        :param interaction: The application command interaction.
        :param user_id: The ID of the user that should be banned.
        :param reason: The reason for the ban. Default is "Not specified".
        """
        try:
            await self.bot.http.ban(user_id, interaction.guild.id, reason=reason)
            user = await self.bot.get_or_fetch_user(int(user_id))
            embed = disnake.Embed(
                title="User Banned!",
                description=f"**{user} (ID: {user_id}) ** was banned by **{interaction.author}**!",
                color=0x9C84EF
            )
            embed.add_field(
                name="Reason:",
                value=reason
            )
            logging.info(f"{user} (ID: {user_id}) was banned by {interaction.author} for {reason}!")
            await interaction.send(embed=embed)
        except Exception as e:
            embed = disnake.Embed(
                title="Error!",
                description="An error occurred while trying to ban the user. Make sure ID is an existing ID that belongs to a user.",
                color=0xE02B2B
            )
            await interaction.send(embed=embed)
            print(e)

    @commands.slash_command(
        name="newrole",
        description="Creates a new role."
    )
    @commands.has_guild_permissions(manage_channels=True)
    @checks.not_blacklisted()
    async def newrole(self, interaction: ApplicationCommandInteraction, *, name: str) -> None:
        """
        Creates a new role.
        :param interaction: The application command interaction.
        :param name: The name of the role.
        """
        try:
            await interaction.guild.create_role(name=name)
            embed = disnake.Embed(
                title="Role Created!",
                description=f"**{role_name.content}** was created by **{interaction.author}**!",
                color=0x9C84EF
            )
            logging.info(f"{role_name.content} was created by {interaction.author}!")
            await interaction.send(embed=embed)
        except:
            embed = disnake.Embed(
                title="Error!",
                description="An error occurred while trying to create the role.",
                color=0xE02B2B
            )
            await interaction.send(embed=embed)


def setup(bot):
    bot.add_cog(Moderation(bot))
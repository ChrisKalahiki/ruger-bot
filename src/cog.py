import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

GUILD_ID = '418089559188832257'

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="test", guild_ids=[GUILD_ID])
    async def test(self, ctx: SlashContext):
        await ctx.send("Hello World!")

    @cog_ext.cog_slash(name="ping", guild_ids=[GUILD_ID])
    async def ping(self, ctx: SlashContext):
        await ctx.send("pong!")

def setup(bot):
    bot.add_cog(Slash(bot))

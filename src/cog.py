import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="test")
    async def _test(self, ctx: SlashContext):
        await ctx.send("Hello World!")

    @cog_ext.cog_slash(name="ping")
    async def _ping(self, ctx: SlashContext):
        await ctx.send("pong!")

def setup(bot):
    bot.add_cog(Slash(bot))

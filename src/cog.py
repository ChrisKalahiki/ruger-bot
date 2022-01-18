import discord, json
from discord.ext import commands
from discord_slash import cog_ext, SlashContext


with open('../pass.json') as f:
    d = json.load(f)

GUILD_ID = d['guildID']

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

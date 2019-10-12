from discord.ext import commands
from discord.ext.commands import command
import random


class EasterEggs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(aliases=["Hype"])
    async def hype(self, ctx):
        hype_links = self.bot.file_manager.get_config('easter_eggs')['hype_links']
        await ctx.send(random.choice(hype_links))

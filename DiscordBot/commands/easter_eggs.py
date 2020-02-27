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

    @command()
    async def hyoe(self, ctx):
        await ctx.send("I am very excitement too:)")

    @command(aliases=["botsnack", "BotSnack", "snack", "Snack"])
    async def botSnack(self, ctx):
        if ctx.message.author.id == 255517263724150787:
            await ctx.send("I have type II diabetes, you know that I can't eat that, Liam.")

        else:
            await ctx.send("I don't take candy from strangers!")

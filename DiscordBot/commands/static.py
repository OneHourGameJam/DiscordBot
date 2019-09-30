from discord.ext import commands
from discord.ext.commands import command


class Static(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @property
    def commands(self):
        return self.bot.config.get('static_commands')

    @command()
    async def about(self, ctx):
        await ctx.send(self.commands['about'])

    @command(aliases=["faq", "FAQ"])
    async def rules(self, ctx):
        await ctx.send(self.commands['rules'])

    @command()
    async def vote(self, ctx):
        await ctx.send(self.commands['vote'])

    @command()
    async def submit(self, ctx):
        await ctx.send(self.commands['submit'])

    @command()
    async def login(self, ctx):
        await ctx.send(self.commands['login'])

    @command(aliases=["issue", "suggestion", "suggestions", "github"])
    async def issues(self, ctx):
        await ctx.send(self.commands['github_issues'])

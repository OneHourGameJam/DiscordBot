from discord.ext import commands
from discord.ext.commands import command
import random


class RandomTheme(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.themes = self.get_themes()

    def get_themes(self):
        file = self.bot.file_manager.read_local('random_themes.txt')
        return [s for s in file.split('\n') if s != '']

    @command(aliases=['randomtheme', 'randomTheme', 'RandomTheme'])
    async def random_theme(self, ctx):
        theme = random.choice(self.themes)
        await ctx.send(f'Your random theme is `{theme}`.')

    @command(aliases=['addrandomtheme', 'addRandomTheme', 'AddRandomTheme'])
    async def add_random_theme(self, ctx):
        theme = ctx.message.content.replace(f'{ctx.prefix}{ctx.invoked_with} ', '').lower()

        if theme.replace(' ', '') != '':
            self.themes = self.get_themes()
            if theme not in self.themes:
                self.bot.file_manager.write_local('random_themes.txt', '\n' + theme, append=True)

                self.themes = self.get_themes()
                await ctx.send(f'Added `{theme}` to random themes!')
            else:
                await ctx.send(f'`{theme}` is already a random theme.')

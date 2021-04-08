import discord.ext.commands as commands
from DiscordBot.commands import API, Static, EasterEggs, RandomTheme


class Bot(commands.Bot):

    def __init__(self, file_manager):
        self.file_manager = file_manager
        super().__init__(commands.when_mentioned_or(self.file_manager.get_config('settings')['prefix']))

    def add_cogs(self):
        self.add_cog(API(self))
        self.add_cog(Static(self))
        self.add_cog(EasterEggs(self))
        self.add_cog(RandomTheme(self))

    async def on_ready(self):
        print('Logged on!')

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        raise error

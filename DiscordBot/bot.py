import discord.ext.commands as commands
from DiscordBot.commands import API


class Bot(commands.Bot):

    def __init__(self, config):
        self.config = config

        prefix = self.config.get('prefix')
        super().__init__(commands.when_mentioned_or(prefix))

        self.add_cog(API(self))

    async def on_ready(self):
        print('Logged on!')

        c_id = self.config.get('debug_channel')
        if c_id is not None:
            channel = self.get_channel(c_id)
            await channel.send('Hello there')

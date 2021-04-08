import DiscordBot as DB
from discord_slash import SlashCommand
import os

file_manager = DB.FileManager(os.path.dirname(os.path.abspath(__file__)))
bot = DB.Bot(file_manager)
slash = SlashCommand(bot, sync_commands=True)
bot.add_cogs()

bot.run(file_manager.get_config('settings')['bot_token'])

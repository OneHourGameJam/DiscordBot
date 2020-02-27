import DiscordBot as DB
import os

file_manager = DB.FileManager(os.path.dirname(os.path.abspath(__file__)))
bot = DB.Bot(file_manager)

bot.run(file_manager.get_config('settings')['bot_token'])

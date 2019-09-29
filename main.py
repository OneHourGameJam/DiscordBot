import DiscordBot as DB
import os

config = DB.ConfigManager(os.path.dirname(os.path.abspath(__file__)) + '/config.json')
bot = DB.Bot(config)

bot.run(config.get('bot_token'))

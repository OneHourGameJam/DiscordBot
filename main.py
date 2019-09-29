import DiscordBot as DB

config = DB.ConfigManager('config.json')
bot = DB.Bot(config)

bot.run(config.get('bot_token'))

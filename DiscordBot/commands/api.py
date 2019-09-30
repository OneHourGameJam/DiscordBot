import json
import requests
from discord.ext import commands
from discord.ext.commands import command
import DiscordBot.backend as backend
import humanfriendly as hf


class API(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def __get_api(self):
        page = requests.get(self.bot.config.get('api_url'))
        content = page.content.decode('UTF-8')
        return json.loads(content)

    @command(aliases=['Time', "TIME", "timeleft", "timeLeft", "TIMELEFT", "Timeleft"])
    async def time(self, ctx):
        api = self.__get_api()
        time_diff = backend.get_time_diff(api)

        if time_diff == 0:
            n = backend.to_ordinal(backend.get_jam_number(api))
            await ctx.send(f"The {n} ohgj starts NOW!")
        else:
            await ctx.send(f"{hf.format_timespan(time_diff)} left until the next jam.")

    @command(aliases=["Theme", "THEME"])
    async def theme(self, ctx):
        api = self.__get_api()
        theme = backend.get_theme(api)

        if theme is None:
            await ctx.send("The theme hasn't been announced yet.")
        else:
            await ctx.send(f"The theme is `{theme}`!")

    @command(aliases=["lasttheme", "LastTheme", "lastTheme"])
    async def last_theme(self, ctx):
        api = self.__get_api()
        theme = backend.get_last_theme(api)
        await ctx.send(f"The previous theme was `{theme}`.")

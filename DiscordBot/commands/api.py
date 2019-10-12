import json
import requests
import humanfriendly as hf
import asyncio
from datetime import datetime as dt
from discord.ext import commands
from discord.ext.commands import command
import DiscordBot.backend as backend


class API(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.announce_jam())

    def __get_api(self):
        page = requests.get(self.bot.file_manager.get_config('1hgj')['api_url'])
        content = page.content.decode('UTF-8')
        return json.loads(content)

    async def announce_jam(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            api = self.__get_api()

            next_jam = backend.get_next_jam_date(api)
            seconds_left = (next_jam - dt.utcnow()).total_seconds()
            # print(seconds_left)

            await asyncio.sleep(60)

    @command(aliases=['Time', "TIME", "timeleft", "timeLeft", "TIMELEFT", "Timeleft", "time_left"])
    async def time(self, ctx):
        api = self.__get_api()
        time_diff = backend.get_time_diff(api)

        if time_diff == 0:
            n = backend.to_ordinal(backend.get_jam_number(api))
            await ctx.send(f"The {n} One Hour Game Jam starts now!")
        elif time_diff > 0:
            await ctx.send(f"{hf.format_timespan(time_diff)} left until the next jam.")
        else:
            time_diff = 3600 - time_diff
            await ctx.send(f"{hf.format_timespan(time_diff)} left.")

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
        await ctx.send(f"The last theme was `{theme}`.")

"""
The main file for the One Hour Game Jam Discord bot.
This file contains every command the bot uses.
"""
from datetime import datetime

import discord
from discord.ext import commands
import random
import datetime
import asyncio

import Config
import JamInfo
import tweetBot
import server

bot = commands.Bot(command_prefix=Config.Prefix)


# region Debug

@bot.command()
async def now():
    if Config.DEBUG:
        await bot.say("Current server time: " + JamInfo.getNow().__str__())


@bot.event
@asyncio.coroutine
def on_ready():
    """
    Prints a message into the debug channel when it goes online
    """
    if Config.DEBUG:
        features = "\nDebug Enabled: {}\nDirectory: {}\nLastTheme Enabled: {}\nEasterEggs Enabled: {" \
                    "}\nRandomTheme Enabled: {}\nTwitterBot Enabled: {}\nJamReminder Enabled: {}"
        enabled_features = features.format(Config.DEBUG, Config.directory_path, Config.usingLastTheme, Config.usingEasterEggs,
                                           Config.usingRandomTheme, Config.usingTwitterBot, Config.usingJamReminder)

        channel = discord.Object(id=Config.DEBUG_channel)
        yield from bot.send_message(channel, "***I have come online (" + JamInfo.getNow().__str__() + ")***" + enabled_features)


# endregion

# region Jam Reminder

def check_time(time_to_compare: datetime.datetime):
    """
    Compares the given time to utc now. It doesn't compare beyond minutes
    :param time_to_compare: datetime object for comparison
    :return: Bool
    """
    utc_now = datetime.datetime.utcnow()
    utc_now = utc_now.replace(second=0, microsecond=0)
    time_to_compare = time_to_compare.replace(second=0, microsecond=0)

    if utc_now == time_to_compare:
        return True
    else:
        return False


@asyncio.coroutine
def jamReminderTask():
    yield from bot.wait_until_ready()

    while not bot.is_closed:

        start_time = "8PM UTC, Midday PST, 3PM EST, 9PM CET and 7AM AEDT."  # Daylight wasting
        # start_time = "8PM UTC, 1 PM PST, 4PM EST, 10PM CET and 6AM ACT." # Daylight savings

        next_jam_date = JamInfo.getUpcomingJamDate()

        tweet_content = "EMPTY"
        send_reminder = False

        # 24 hour reminder
        if check_time(next_jam_date - datetime.timedelta(hours=24)):
            tweet_content = "1 Hour Game Jam starts in 24h! That's at " + start_time + " https://onehourgamejam.com " + Config.twitter_hashtags

        # 16 hour reminder
        elif check_time(next_jam_date - datetime.timedelta(hours=16)):
            tweet_content = "1 Hour Game Jam starts in 16h! That's at " + start_time + " https://onehourgamejam.com " + Config.twitter_hashtags

        # 8 hour reminder
        elif check_time(next_jam_date - datetime.timedelta(hours=8)):
            tweet_content = "1 Hour Game Jam starts in 8h! That's at " + start_time + " https://onehourgamejam.com " + Config.twitter_hashtags

        # 4 hour reminder
        elif check_time(next_jam_date - datetime.timedelta(hours=4)):
            tweet_content = "1 Hour Game Jam starts in 4h! Participate at https://onehourgamejam.com " + Config.twitter_hashtags

        # 2 hour reminder
        elif check_time(next_jam_date - datetime.timedelta(hours=2)):
            tweet_content = "1 Hour Game Jam starts in 2h! Participate at https://onehourgamejam.com " + Config.twitter_hashtags

        # 1 hour reminder
        elif check_time(next_jam_date - datetime.timedelta(hours=1)):
            tweet_content = "1 Hour Game Jam starts in 1h! Join us on Discord at https://discord.gg/J86uTu9 " + Config.twitter_hashtags
            send_reminder = True

        # 20 min reminder
        elif check_time(next_jam_date - datetime.timedelta(minutes=20)):
            tweet_content = "1 Hour Game Jam starts in 20 minutes! Join us on Discord at https://discord.gg/J86uTu9 " + Config.twitter_hashtags

        # START reminder
        elif check_time(next_jam_date):
            jam_number = JamInfo.getCurrentJamNumber()
            jam_theme = JamInfo.getCurrentTheme()
            tweet_content = "1 hour game jam " + jam_number + " started. The theme is: '" + jam_theme + "'. Participate at https://onehourgamejam.com " + Config.twitter_hashtags

        # ---- Twitter ----
        if Config.usingTwitterBot and Config.usingAutoTwitterBot and tweet_content != "EMPTY":
            tweetBot.tweet(tweet_content)
            yield from bot.send_message(discord.Object(id=Config.DEBUG_modChannel), "<@111890906055020544>Tweet sent\n||" + tweet_content + "||")

        # ---- Send Jam Reminder ----
        if Config.usingJamReminder and send_reminder:
            yield from bot.send_message(discord.Object(id=Config.reminder_JamChannel),
                        "@everyone The One Hour Game Jam starts within an hour! Hype<:lime:322433693111287838>!!")

        elif not Config.usingJamReminder and send_reminder:
            yield from bot.send_message(discord.Object(id=Config.DEBUG_modChannel),
                        ":speak_no_evil: I tried sending out a reminder but Liam was like \"urm no u aren't\" :speak_no_evil:")

        yield from asyncio.sleep(60)  # Run task every 60 seconds


# endregion

# region Dynamic Commands

# region Next Jam API
'''
ABOUT:
Contains all of the commands using the One Hour Game Jam API (code in JamInfo.py)
'''


@bot.command(aliases=["Theme", "THEME"])
async def theme():
    current_theme = JamInfo.getCurrentTheme()  # Get the theme of the ongoing jam

    if current_theme == "":
        response = Config.commands_themeNotAnnounced  # If the ongoing jam JSON string is empty there isn't an ongoing jam ergo the theme hasn't been announced yet
    else:
        response = Config.commands_theme.format(current_theme)

    await bot.say(response)


@bot.command(aliases=["lasttheme", "LastTheme"])
async def lastTheme():
    if Config.usingLastTheme:
        await bot.say(Config.commands_getLastTheme.format(JamInfo.getLastTheme()))


@bot.command(aliases=['Time', "TIME", "timeleft", "timeLeft", "TIMELEFT", "Timeleft"])
async def time():
    time_diff = JamInfo.getTimeDiff()  # Get the time remaining
    response = Config.commands_getTime_Upcoming

    if time_diff < 0:  # If time_diff is negative the jam has already started
        time_diff = 3600 + time_diff  # Calculate the time until the jam ends
        response = Config.commands_getTime_Ongoing

    formatted_diff = JamInfo.formatTime(time_diff)  # Get the formatted array

    if formatted_diff[0] != "":
        response = response.format(
            formatted_diff[0] + " " + formatted_diff[1] + " " + formatted_diff[2])  # Day + Hour + Min
    elif formatted_diff[1] != "":
        response = response.format(formatted_diff[1] + " " + formatted_diff[2])  # Hour + Min
    elif formatted_diff[2] != "":
        response = response.format(formatted_diff[2] + " " + formatted_diff[3])  # Min + Sec
    else:
        response = response.format(formatted_diff[3])  # Sec

    await bot.say(response)


@bot.command(aliases=[], pass_context=True)
async def setAnnouncements(ctx, option):
    member = ctx.message.author
    if Config.adminRoleName.lower() in [y.name.lower() for y in member.roles]:  # Check if user has correct role

        if option.lower() == "on":
            Config.usingJamReminder = True
            Config.usingAutoTwitterBot = True
            await bot.say("Announcements: **On**")

        elif option.lower() == "off":
            Config.usingJamReminder = False
            Config.usingAutoTwitterBot = False
            await bot.say("Announcements: **Off**")
        else:
            await bot.say("Unknown command: \"" + option + "\"")

    else:
        await bot.say("You do not have the correct role.")

# endregion

# region Random Theme

@bot.command(aliases=["randomtheme", "RandomTheme", "Randomtheme"])
async def randomTheme():
    if Config.usingRandomTheme:
        await bot.say("Your random theme is: " + server.getRandomTheme())


@bot.command(aliases=["addrandomtheme", "AddRandomTheme", "Addrandomtheme"], pass_context=True)
async def addRandomTheme(ctx):
    message = str(ctx.message.content)

    name = message.lower().replace("!addrandomtheme ", "")
    name = name.replace("!addrandomtheme", "")

    name = name.replace("!AddRandomTheme ", "")
    name = name.replace("!AddRandomTheme", "")

    name = name.replace("!Addrandomtheme ", "")
    name = name.replace("!Addrandomtheme", "")

    name = name.replace("!addRandomTheme ", "")
    name = name.replace("!addRandomTheme", "")

    name = name.replace('"', "")

    if Config.usingRandomTheme:
        if name != "":
            server_hash = server.generateHash(name)
            server.addRandomTheme(name, server_hash)
            await bot.say("Added '" + name + "' to random themes.")
        else:
            await bot.say("Random theme cannot be an empty string")


# endregion

# region Twitter
'''
ABOUT:
Commands using the Twitter API (code in tweetBot.py)
'''


@bot.command(pass_context=True)
async def tweetReminder(ctx, member: discord.Member = None):
    if Config.usingTwitterBot:
        if member is None:
            member = ctx.message.author

        if Config.adminRoleName.lower() in [y.name.lower() for y in member.roles]:  # Check if the user is a moderator
            offset = datetime.datetime.utcnow() - server.getLastTweet()  # Get the time since last tweet

            if offset.total_seconds() >= Config.twitter_timeSinceTweet:
                time_diff = JamInfo.getTimeDiff()  # Get the time remaining

                if time_diff < 0:  # If timeDiff is negative the jam has already started -- Too late to tweet
                    await bot.say("The jam has already started -- NOT TWEETING")

                formatted_diff = JamInfo.formatTime(time_diff)  # Get the formatted array

                if formatted_diff[0] != "":
                    time_left = formatted_diff[0] + " " + formatted_diff[1] + " " + formatted_diff[2]  # D + h + m
                elif formatted_diff[1] != "":
                    time_left = formatted_diff[1] + " " + formatted_diff[2]  # h + m
                elif formatted_diff[2] != "":
                    time_left = formatted_diff[2] + " " + formatted_diff[3]  # m + s
                else:
                    time_left = formatted_diff[3]  # s

                date = JamInfo.getUpcomingJamDate()

                value = str.format(
                    "The #1hgj starts in {0} (Sat {1} UTC)! More info at onehourgamejam.com #gamedev #indiedev #gamejam",
                    time_left, date)
                value_len = value.count("")

                if value_len <= 280:
                    await bot.say(tweetBot.tweet(value))
                else:
                    await bot.say("Tweet error: Too many characters to tweet")

            else:
                await bot.say("Not enough time has passed since last tweet (" + str(
                    round((28800 - offset.total_seconds()) / 3600, 3)) + "h left)")
        else:
            print("Wrong role")


# endregion

# endregion

# region Static Commands

'''
ABOUT:
Commands that only do one thing: Print a static string
in the chat every time they're called. These wont be documented
because their functions are pretty explicit.
'''

# region One Hour Game Jam Commands

'''
ABOUT:
Static commands meant to to aid newcomers
with links to the One Hour Game Jam website.

You can edit the content of these commands in Config.py
'''

bot.remove_command("help")  # discord.py comes with a default definition of 'help' which we need to remove


@bot.command(aliases=["help", "Help"])
async def commands():
    await bot.say(Config.commands_botCommands)


@bot.command()
async def about():
    await bot.say(Config.commands_aboutOHGJ)


@bot.command(aliases=["faq", "FAQ"])
async def rules():
    await bot.say(Config.commands_rules)


@bot.command()
async def vote():
    await bot.say(Config.commands_vote)


@bot.command()
async def submit():
    await bot.say(Config.commands_submit)


@bot.command()
async def login():
    await bot.say(Config.commands_login)


@bot.command(aliases=["Shirt", "SHRIT", "merch", "MERCH"])
async def shirt():
    await bot.say(Config.commands_merch)


@bot.command(aliases=["issue", "suggestion", "suggestions", "github"])
async def issues():
    await bot.say("Submit issues or suggestions here: " + Config.links_GitHubIssues)


# endregion

# region Easter Egg Commands

'''
ABOUT:
Static commands that are in here just
for fun and have no explicit function.
'''


@bot.command(pass_context=True)
async def hyoe(ctx, member: discord.Member = None):
    if Config.usingEasterEggs:
        if member is None:
            member = ctx.message.author
        await bot.say(":)")
        await bot.send_message(member, "That command will only be implemented if you vote for it here: " + Config.links_Hyoe_Github)


@bot.command(aliases=["Hype"])
async def hype():
    if Config.usingEasterEggs:
        link = random.choice(Config.easterEggs_hypeLinks)
        await bot.say(link)


@bot.command(aliases=["PANIC"])
async def panic():
    if Config.usingEasterEggs:
        link = random.choice(Config.easterEggs_panicLinks)
        await bot.say(link)


@bot.command(aliases=["11-2-2019"])
async def neverforgetti():
    if Config.usingEasterEggs:
        await bot.say("https://cdn.discordapp.com/attachments/544558735071379466/544583034310230039/4a333bac7f4d10b8bac58046faa3b238.png")


@bot.command()
async def hypeAll():
    if Config.usingEasterEggs:
        await bot.say(', '.join(Config.easterEggs_hypeLinks))


@bot.command(aliases=["conquerworld", "CONQUERWORLD"])
async def conquerWorld():
    if Config.usingEasterEggs:
        await bot.say("https://www.youtube.com/watch?v=XJYmyYzuTa8")


@bot.command()
async def lime():
    if Config.usingEasterEggs:
        await bot.say("What is life? <:lime:322433693111287838>")


@bot.command()
async def limes():
    if Config.usingEasterEggs:
        await bot.say("What's a limes? :confused:")


@bot.command(aliases=["hypeTrain", "HypeTrain"])
async def hypetrain():
    if Config.usingEasterEggs:
        await bot.say("https://youtu.be/gMkrvTraVZ0")


@bot.command(aliases=["weirdHypeTrain", "WeirdHypeTrain"])
async def weirdhypetrain():
    if Config.usingEasterEggs:
        await bot.say("http://youtu.be/lSxh-UK7Ays")


@bot.command(aliases=["slovakhypetrain", "SlovakHypeTrain"])
async def slovakHypeTrain():
    if Config.usingEasterEggs:
        await bot.say("https://www.youtube.com/watch?v=zpGU355C0ak")


@bot.command()
async def hypeSquad():
    if Config.usingEasterEggs:
        await bot.say("https://cdn.discordapp.com/attachments/326736434763661312/419582034202198016/kedengmeme.gif")


@bot.command(aliases=["botsnack", "BotSnack", "snack", "Snack"], pass_context = True)
async def botSnack(ctx):
    if Config.usingEasterEggs:
        if ctx.message.author.id == "255517263724150787":
            await bot.say("I have type II diabetes, you know that I can't eat that, Liam.")

        else:
            await bot.say("I don't take candy from strangers!")





# endregion

# endregion

bot.loop.create_task(jamReminderTask())
bot.run(Config.bot_key)

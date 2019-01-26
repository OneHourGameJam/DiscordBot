'''
ABOUT:
The main file for the One Hour Game Jam Discord bot.
This file contains every command the bot uses.
'''
import discord
from discord.ext import commands
import random
import datetime
import asyncio
import io

import Config
import JamInfo
import tweetBot
import server

bot = commands.Bot(command_prefix="!")

#region Debug

@bot.command()
async def now():
    # Gets the 'now' from the One Hour Game Jam server
    if(Config.DEBUG):
        await bot.say("Current server time: " + JamInfo.getNow().__str__())

@bot.event
@asyncio.coroutine
def on_ready():

    #Prints a message into a custom channel when it goes online
    if(Config.DEBUG):
        enabledFeatures = "\nDebug Enabled: {}\nDirectory: {}\nLastTheme Enabled: {}\nRandomTheme Enabled: {}\nEasterEggs Enabled: {}\nTwitterBot Enabled: {}\nJamReminder Enabled: {}".format(
        Config.DEBUG, Config.dir_path, Config.usingLastTheme, Config.usingRandomTheme, Config.usingEasterEggs, Config.usingTwitterBot, Config.usingJamReminder)

        channelID = discord.Object(id=Config.DEBUG_channel) # Get the channel ID of the debug channel
        yield from bot.send_message(channelID, "***I have come online ("  + JamInfo.getNow().__str__() + ")***" + enabledFeatures)

#endregion

#region Jam Reminder

def checkTime(time : datetime.datetime):
    now = datetime.datetime.utcnow()
    now = now.replace(second=0, microsecond=0)
    time = time.replace(second=0, microsecond=0)

    if now == time:
        return True
    else:
        return False

@asyncio.coroutine
def jamReminderTask():
    yield from bot.wait_until_ready()

    while not bot.is_closed:

        if Config.usingJamReminder:
            startTime = "8PM UTC, Midday PST, 3PM EST, 9PM CET and 7AM AEDT." #Daylight wasting
            #startTime = "8PM UTC, 1 PM PST, 4PM EST, 10PM CET and 6AM ACT." # Daylight savings

            nextJamDate = JamInfo.getUpcomingJamDate()

            #24 hour reminder
            if checkTime(nextJamDate - datetime.timedelta(hours=24)):
                tweetBot.tweet("1 Hour Game Jam starts in 24h! That's at " + startTime + " https://onehourgamejam.com " + Config.twitter_hashtags)
                yield from bot.send_message(discord.Object(id=Config.DEBUG_modChannel), "<@111890906055020544> 24h Tweet sent")
            #16 hour reminder
            elif checkTime(nextJamDate - datetime.timedelta(hours=16)):
                tweetBot.tweet("1 Hour Game Jam starts in 16h! That's at " + startTime + " https://onehourgamejam.com " + Config.twitter_hashtags)
                yield from bot.send_message(discord.Object(id=Config.DEBUG_modChannel), "<@111890906055020544> 16h Tweet sent")
            #8 hour reminder
            elif checkTime(nextJamDate - datetime.timedelta(hours=8)):
                tweetBot.tweet("1 Hour Game Jam starts in 8h! That's at " + startTime + " https://onehourgamejam.com " + Config.twitter_hashtags)
                yield from bot.send_message(discord.Object(id=Config.DEBUG_modChannel), "<@111890906055020544> 8h Tweet sent")
            #4 hour reminder
            elif checkTime(nextJamDate - datetime.timedelta(hours=4)):
                tweetBot.tweet("1 Hour Game Jam starts in 4h! Participate at https://onehourgamejam.com " + Config.twitter_hashtags)
                yield from bot.send_message(discord.Object(id=Config.DEBUG_modChannel), "<@111890906055020544> 4h Tweet sent")
            #2 hour reminder
            elif checkTime(nextJamDate - datetime.timedelta(hours=2)):
                tweetBot.tweet("1 Hour Game Jam starts in 2h! Participate at https://onehourgamejam.com " + Config.twitter_hashtags)
                yield from bot.send_message(discord.Object(id=Config.DEBUG_modChannel), "<@111890906055020544> 2h Tweet sent")
            #1 hour reminder
            elif checkTime(nextJamDate - datetime.timedelta(hours=1)):
                tweetBot.tweet("1 Hour Game Jam starts in 1h! Join us on Discord at https://discord.gg/J86uTu9 " + Config.twitter_hashtags)
                yield from bot.send_message(discord.Object(id=Config.reminder_JamChannel), "@everyone The One Hour Game Jam starts within an hour! Hype<:lime:322433693111287838>!!")
                yield from bot.send_message(discord.Object(id=Config.DEBUG_modChannel), "<@111890906055020544> 1h Tweet sent")
            #20 min reminder
            elif checkTime(nextJamDate - datetime.timedelta(minutes=20)):
                tweetBot.tweet("1 Hour Game Jam starts in 20 minutes! Join us on Discord at https://discord.gg/J86uTu9 " + Config.twitter_hashtags)
                yield from bot.send_message(discord.Object(id=Config.DEBUG_modChannel), "<@111890906055020544> 20min Tweet sent")
            #START reminder
            elif checkTime(nextJamDate):
                tweetBot.tweet("1 hour game jam " + JamInfo.getCurrentJamNumber() + " started. The theme is: '" + JamInfo.getCurrentTheme() + "'. Participate at https://onehourgamejam.com " + Config.twitter_hashtags)
                yield from bot.send_message(discord.Object(id=Config.DEBUG_modChannel), "<@111890906055020544> Jam start Tweet sent")

        yield from asyncio.sleep(60)  # Run task every 60 seconds
#endregion

#region Dynamic Commands

#region Next Jam API
'''
ABOUT:
Contains all of the commands using the One Hour Game Jam API (code in JamInfo.py)
'''

@bot.command(aliases=["Theme", "THEME"])
async def theme():
    response = ""
    theme = JamInfo.getCurrentTheme() # Get the theme of the ongoing jam

    if(theme == ""):
        response = Config.commands_themeNotAnnounced # If the ongoing jam JSON string is empty there isn't an ongoing jam ergo the theme hasn't been announced yet
    else:
        response = Config.commands_theme.format(theme)

    await bot.say(response)

@bot.command(aliases=["lasttheme", "LastTheme"])
async def lastTheme():
    if(Config.usingLastTheme):
        await bot.say(Config.commands_getLastTheme.format(JamInfo.getLastTheme()))

@bot.command(aliases=['Time', "TIME","timeleft", "timeLeft", "TIMELEFT", "Timeleft"])
async def time():
    timeDiff = JamInfo.getTimeDiff() # Get the time remaining
    response = Config.commands_getTime_Upcoming

    if(timeDiff < 0): # If timeDiff is negative the jam has already started
        timeDiff = 3600 + timeDiff # Calculate the time until the jam ends
        response = Config.commands_getTime_Ongoing

    formattedDiff = JamInfo.formatTime(timeDiff) # Get the formatted array

    if(formattedDiff[0] != ""): response =  response.format(formattedDiff[0] + " " + formattedDiff[1] + " " + formattedDiff[2]) # Day + Hour + Min
    elif(formattedDiff[1] != ""): response =  response.format(formattedDiff[1] + " " + formattedDiff[2]) # Hour + Min
    elif(formattedDiff[2] != ""): response =  response.format(formattedDiff[2] + " " + formattedDiff[3]) # Min + Sec
    else: response = response.format(formattedDiff[3]) # Sec

    await bot.say(response)
#endregion

#region Random Theme

@bot.command(aliases=["randomtheme", "RandomTheme", "Randomtheme"])
async def randomTheme():
    if(Config.usingRandomTheme):
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

    if (Config.usingRandomTheme):
        if(name != ""):
            hash = server.generateHash(name)
            server.addRandomTheme(name, hash)
            await bot.say("Added '" + name + "' to random themes.")
        else:
            await bot.say("Random theme cannot be an empty string")

#endregion

#region Twitter
'''
ABOUT:
Commands using the Twitter API (code in tweetBot.py)
'''
@bot.command(pass_context=True)
async def tweetReminder(ctx, member : discord.Member = None):
    if(Config.usingTwitterBot):
        if member is None:
            member = ctx.message.author

        if "moderator" in [y.name.lower() for y in member.roles]: # Check if the user is a moderator
            offset = datetime.datetime.utcnow() - server.getLastTweet() # Get the time since last tweet

            if(offset.total_seconds() >= Config.twitter_timeSinceTweet): # Has **Config.twitter_timeSinceTweet** passed since the last tweet?
                timeDiff = JamInfo.getTimeDiff()  # Get the time remaining
                timeLeft = ""

                if (timeDiff < 0):  # If timeDiff is negative the jam has already started -- Too late to tweet
                    await bot.say("The jam has already started -- NOT TWEETING")

                formattedDiff = JamInfo.formatTime(timeDiff)  # Get the formatted array

                if (formattedDiff[0] != ""):timeLeft = formattedDiff[0] + " " + formattedDiff[1] + " " + formattedDiff[2]  # Day + Hour + Min
                elif (formattedDiff[1] != ""): timeLeft = formattedDiff[1] + " " + formattedDiff[2] # Hour + Min
                elif (formattedDiff[2] != ""): timeLeft = formattedDiff[2] + " " + formattedDiff[3]  # Min + Sec
                else: timeLeft = formattedDiff[3]  # Sec

                date = JamInfo.getUpcomingJamDate()

                value = str.format("The #1hgj starts in {0} (Sat {1} UTC)! More info at onehourgamejam.com #gamedev #indiedev #gamejam", timeLeft, date)
                valueLen = value.count("")

                if valueLen <= 280:
                    await bot.say(tweetBot.tweet(value))
                else:
                    await bot.say("Tweet error: Too many characters to tweet")

            else:
                await bot.say("Not enough time has passed since last tweet (" + str(round((28800 - offset.total_seconds()) / 3600, 3)) + "h left)")
        else:
            print("Wrong role")

#endregion

#endregion

#region Static Commands

'''
ABOUT:
Commands that only do one thing: Print a static string
in the chat every time they're called. These wont be documented
because their functions are pretty explicit.
'''

#region One Hour Game Jam Commands

'''
ABOUT:
Static commands meant to to aid newcomers
with links to the One Hour Game Jam website.

You can edit the content of these commands in Config.py
'''

bot.remove_command("help")  #The discord.py library comes with a default definition of the 'help' command so we remove the pre-defined one before we can define a new one in the next line
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

#endregion

#region Easter Egg Commands

'''
ABOUT:
Static commands that are in here just
for fun and have no explicit function.
'''

@bot.command(pass_context=True)
async def hyoe(ctx, member : discord.Member = None):
    if(Config.usingEasterEggs):
        if member is None:
            member = ctx.message.author
        await bot.say(":(")
        await bot.send_message(member, "That command will only be implemented if you vote for it here: " + Config.links_GitHubIssues)

@bot.command(aliases=["Hype"])
async def hype():
    if(Config.usingEasterEggs):
        link = random.choice(Config.easterEggs_hypeLinks)
        await bot.say(link)

@bot.command()
async def hypeAll():
    if (Config.usingEasterEggs):
        await bot.say(', '.join(Config.easterEggs_hypeLinks))

@bot.command()
async def conquerWorld():
    if (Config.usingEasterEggs):
        await bot.say(Config.easterEggs_conquerWorld)

@bot.command()
async def hottestManAlive():
    if (Config.usingEasterEggs):
        await bot.say(Config.easterEggs_hottestManAlive)

@bot.command()
async def eminem():
    if (Config.usingEasterEggs):
        await bot.say(Config.easterEggs_eminem)

@bot.command()
async def lime():
    if (Config.usingEasterEggs):
        await bot.say(Config.easterEggs_lime)

@bot.command()
async def limes():
    if (Config.usingEasterEggs):
        await bot.say(Config.easterEggs_limes)

@bot.command(aliases=["hypeTrain", "HypeTrain"])
async def hypetrain():
    if (Config.usingEasterEggs):
        await bot.say(Config.easterEggs_hypeTrain)

@bot.command(aliases=["weirdHypeTrain", "WeirdHypeTrain"])
async def weirdhypetrain():
    if (Config.usingEasterEggs):
        await bot.say(Config.easterEggs_weirdHypeTrain)

@bot.command(aliases=["slovakhypetrain", "SlovakHypeTrain"])
async def slovakHypeTrain():
    if (Config.usingEasterEggs):
        await bot.say(Config.easterEggs_slovakHypeTrain)

@bot.command()
async def panic():
    if (Config.usingEasterEggs):
        await bot.say(Config.easterEggs_panic)

@bot.command()
async def hypeSquad():
    if (Config.usingEasterEggs):
        await bot.say(Config.easterEggs_hypeSquad)

@bot.command(aliases = ["botsnack", "BotSnack", "snack", "Snack"])
async def botSnack():
    if (Config.usingEasterEggs):
        await bot.say(Config.easterEggs_snack)
#endregion

#endregion

bot.loop.create_task(jamReminderTask())
bot.run(Config.bot_key)

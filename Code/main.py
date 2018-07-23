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
        channelID = discord.Object(id=Config.DEBUG_channel) # Get the channel ID of the debug channel
        yield from bot.send_message(channelID, "I have come online. "  + JamInfo.getNow().__str__())

#endregion

#region Jam Reminder
# function for the bot that will be called every 60 minutes.
@asyncio.coroutine
def jamReminderTask():
    yield from bot.wait_until_ready()

    while not bot.is_closed:
        # get the current datetime
        now = datetime.datetime.utcnow()
        dtprint=now.strftime("%A %H:%M") ## datetime for printing
        dtcheck=now.strftime("%a %H") ## dateime object for checking
        # check if the time is right
        if dtcheck== "Sat 20":
            channel = discord.Object(id='307620502158049281')   ## this is the 1hgj discord announcement channel

            timeDiff = JamInfo.getTimeDiff()  # Get the time remaining
            formattedDiff = JamInfo.formatTime(timeDiff)  # Get the formatted array

            yield from bot.send_message(channel, "@everyone It is " + str(dtprint) + ". The One Hour Game Jam start in " + formattedDiff[2] + " and " + formattedDiff[3] + ".")
        yield from asyncio.sleep(Config.jamReminder_check) # Run task every **jamReminder_check** seconds
#endregion

#region Dynamic Commands

#region Next Jam API
'''
ABOUT:
Contains all of the commands using the One Hour Game Jam API (code in JamInfo.py)
'''

@bot.command(aliases=["Theme", "THEME"])
async def theme():
    response = JamInfo.getCurrentTheme() # Get the theme of the ongoing jam

    if(response == ""):
        response = Config.commands_themeNotAnnounced # If the ongoing jam JSON string is empty there isn't an ongoing jam ergo the theme hasn't been announced yet

    await bot.say(response)

@bot.command(aliases=["lasttheme", "LastTheme"])
async def lastTheme():
    if(Config.usingLastTheme):
        await bot.say(Config.commands_getLastTheme.format(JamInfo.getLastTheme()))

@bot.command(aliases=['Time', "TIME"])
async def time():
    timeDiff = JamInfo.getTimeDiff() # Get the time remaining
    response = Config.commands_getTime_Upcoming

    if(timeDiff < 0): # If timeDiff is negative the jam has already started
        timeDiff = 3600 - timeDiff # Calculate the time until the jam ends
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
        await bot.say("Your random thmee is: " + server.getRandomTheme())

@bot.command(aliases=["addrandomtheme", "AddRandomTheme", "Addrandomtheme"])
async def addRandomTheme(name : str):
    if (Config.usingRandomTheme):
        name = name.lower()
        hash = server.generateHash(name)

        server.addRandomTheme(name, hash)

        await bot.say("Added '" + name + "' to random themes.")

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

#endregion

#region Easter Egg Commands

'''
ABOUT:
Static commands that are in here just
for fun and have no explicit function.
'''

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
#endregion

#endregion

bot.loop.create_task(jamReminderTask())
bot.run(Config.bot_key)

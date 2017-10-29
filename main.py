import discord
from discord.ext import commands
from datetime import datetime

import functions
import logging
import server
import tweetBot



logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = commands.Bot(command_prefix="!")


client = discord.Client()

bot.remove_command("help")


@bot.command()
async def time():
    response = functions.getJamInfo(1)
    await bot.say(response)

@bot.command()
async def theme():
    response = "The theme " + functions.getJamInfo(0)
    await bot.say(response)

@bot.command()
async def randomTheme():
    await bot.say("Your random theme is: " + server.getRandomTheme())

@bot.command()
async def lime():
    await bot.say("What is life? <:lime:322433693111287838>")

@bot.command()
async def limes():
    await bot.say("What's a limes? :confused:")

@bot.command(pass_context=True)
async def hype(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.message.author

    channel = ctx.message.channel

    #await bot.send_file(channel, "images/hypeTrain.png")
    await bot.send_message(channel, "https://goo.gl/5TKpck")

@bot.command(pass_context=True)
async def tweetReminder(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.message.author

    channel = ctx.message.channel

    if "moderator" in [y.name.lower() for y in member.roles]:
        offset =  datetime.utcnow() - server.getLastTweet()

        if(offset.total_seconds() >= 28800): # 8 hours
            timeleft = functions.getJamInfo(1).replace(" left until the next jam.", "")
            day = functions.getUpcomingJamLong(2).replace("\"", "")

            server.changeLastTweet()

            await bot.say(tweetBot.tweet("The #gamejam starts in " + timeleft + " (Sat " + day + " UTC)! More info at onehourgamejam.com #gamedev #indiedev #1hgj"))

        else:
            await bot.say("Not enough time has passed since last tweet (" + str(round((28800 - offset.total_seconds()) / 3600, 3)) + "h left)")
    else:
        print("Wrong role")


@bot.command()
async def hypetrain():
    await bot.say("https://youtu.be/gMkrvTraVZ0")
	
@bot.command()
async def weirdhypetrain():
    await bot.say("https://www.youtube.com/watch?v=XpbTI4zN1FY")



#@bot.command()
#async def help():
#    await bot.say("You have found me!")

@bot.command()
async def addRandomTheme(name : str):
    response = "If you see me, something went wrong"

    name = name.lower()
    hash = server.generateHash(name)

    if (False == True):
    #if(server.checkBlacklist(name) == True):
            response = "Blacklisted word found in theme."
    else:
        server.addRandomTheme(name, hash)
        response = "Added '" + name + "' to random themes."

    await bot.say(response)


# --------------Static Text Commands------------

@bot.command()
async def vote():
    response = "Vote on the next theme here: http://onehourgamejam.com/?page=themes, **if you don't have an account yet, type __!login__**"
    await bot.say(response)

@bot.command()
async def submit():
    response = "Submit your game here: http://onehourgamejam.com/?page=submit, **if you don't have an account yet, type __!login__**"
    await bot.say(response)

@bot.command()
async def login():
    response = "If you don't have an account yet or if you aren't logged in go here: http://onehourgamejam.com/?page=login"
    await bot.say(response)

@bot.command()
async def commands():
    response = "```Commands:\n\n!about\n!commands\n\n!time\n!theme\n\n!randomTheme\n!addRandomTheme THEME\n\n!submit\n!vote\n!login\n\n!tweetReminder (Mod only)```"#\n\n\nWrite '!help COMMAND' for more info.```"
    await bot.say(response)

@bot.command()
async def about():
    response = "The One Hour Game Jam happens every Saturday at 20:00 UTC and ends at 21:00 UTC. You have until the next jam to submit your game.\nJoin us, learn and just have fun!"
    await bot.say(response)


bot.run("")


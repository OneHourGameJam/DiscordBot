"""
ABOUT:
Stores custom variables the bot uses
"""
import os
dir_path = os.path.dirname(os.path.realpath(__file__)) # The project directory

#region DEBUG
DEBUG = True
DEBUG_channel = '394169935510896643'
DEBUG_reminder_lastReminderFile = dir_path + "/DEBUG/JamReminder.txt"

DEBUG_modChannel = '376327006406836224'
#endregion

#region Enabling Features
usingLastTheme = True
usingRandomTheme = True
usingEasterEggs = True
usingTwitterBot = True
usingJamReminder = True
#endregion

#region Jam Reminder
reminder_JamChannel = '307620502158049281'
reminder_lastJamReminderFile = dir_path + "/BotFiles/JamReminder.txt"
reminder_JamTime = "Sat 19"

reminder_lastVoteReminderFile = dir_path + "/BotFiles/VoteReminder.txt"
reminder_VoteChannel = '285133441937440770'
#endregion

#region Discord API keys
bot_key = "" # The Discord bot key used in bot.run
#endregion

#region Twitter API keys

# The minimum amount that needs to pass until a new tweet is allowed (in seconds)
twitter_timeSinceTweet = 28800 # Default: 28800 sec => 8 hours

# Keys used in tweetbot.py
twitter_consumerKey = ""
twitter_consumerSecret = ""
twitter_accessToken = ""
twitter_tokenSecret = ""
#endregion

#region Server config
server_secretKey = ""

server_changeLastTweetURL = "http://devillime.com/ohgj/bot/changelasttweet.php?"
server_displayLastTweetURL = "http://devillime.com/ohgj/bot/displaylasttweet.php"

server_randomThemeURL = "http://devillime.com/ohgj/bot/addtheme.php?"
server_displayThemeURL = "http://devillime.com/ohgj/bot/displaytheme.php"
#endregion

#region Dynamic Command Responses
commands_themeNotAnnounced = "The theme hasn't been announced yet."
commands_theme = "The theme is: \"{}\""
commands_getLastTheme = "The previous jam's theme was: '{}'"
commands_getTime_Upcoming = "{} left until the next jam."
commands_getTime_Ongoing = "{} left."
#endregion

#region One Hour Game Jam Links
links_API = "https://onehourgamejam.com/api/nextjam/" # The link to the NextJam API

links_rules = "https://onehourgamejam.com/?page=rules" # The link to the rules page
links_themes = "https://onehourgamejam.com/?page=themes" # The link the the theme voting page
links_submit = "https://onehourgamejam.com/?page=submit" # The link to the game submission page
links_login = "https://onehourgamejam.com/?page=login" # The link to the log in/sign up page

links_GitHubIssues = "https://github.com/OneHourGameJam/OneHourGameJam-discord-bot/issues/2"
#endregion

#region Static commands

# A list of bot commands
commands_botCommands = \
        "```" \
        "Commands:\n\n" \
 \
        "!about\n" \
        "!rules\n\n" \
 \
        "!time\n" \
        "!theme\n" \
        "!lastTheme\n\n" \
 \
        "!randomTheme\n" \
        "!addRandomTheme THEME\n" \
        "!randomThemeVoting\n\n" \
 \
        "!submit\n" \
        "!vote\n" \
        "!login\n\n" \
 \
        "!tweetReminder (Mod only)" \
        "```"
commands_aboutOHGJ = "The One Hour Game Jam happens every Saturday at 20:00 UTC and ends at 21:00 UTC. You have until the next jam to submit your game." \
                     "\nJoin us, learn and just have fun!"
commands_rules = "Rules & FAQ: " + links_rules
commands_vote = "Vote on the next theme here: " + links_themes + ", **if you don't have an account yet, type __!login__**"
commands_submit = "Submit your game here: " + links_submit + " , **if you don't have an account yet, type __!login__**"
commands_login = "If you don't have an account yet or if you aren't logged in go here: " + links_login

commands_merch = "There are many online tshirt printing services available, e.g. spreadshirt, shirtinator or shirtcity.\n" \
    "Feel free to use a logo from https://onehourgamejam.com/?page=assets and create your own design.\n\n" \
\
    "If you just want to order a finished shirt, you can use this finished design: https://goo.gl/HybjKA\n\n" \
\
    "OneHourGamejam is not affiliated with any of the listed printing services and we get no profit when you order a shirt from them."

#region Easter Eggs

#The different links the !hype command prints
easterEggs_hypeLinks = ["https://goo.gl/5TKpck", "https://youtu.be/gMkrvTraVZ0", "http://youtu.be/lSxh-UK7Ays",
"https://cdn.discordapp.com/attachments/326736434763661312/419582034202198016/kedengmeme.gif", "https://www.youtube.com/watch?v=zpGU355C0ak", "https://www.youtube.com/watch?v=s6E3xVz01bw", "https://www.youtube.com/watch?v=FDs6dADBmI0"]
easterEggs_conquerWorld = "https://www.youtube.com/watch?v=XJYmyYzuTa8"
easterEggs_hottestManAlive = "http://devillime.com/uploads/image/Gilmour.jpg"
easterEggs_eminem = "Chicka, chicka, chicka, Slim Shady\nhttps://www.youtube.com/watch?v=IdS3WVYr834"
easterEggs_lime = "What is life? <:lime:322433693111287838>"
easterEggs_limes = "What's a limes? :confused:"
easterEggs_hypeTrain = "https://youtu.be/gMkrvTraVZ0"
easterEggs_weirdHypeTrain =  "http://youtu.be/lSxh-UK7Ays"
easterEggs_slovakHypeTrain = "https://www.youtube.com/watch?v=zpGU355C0ak"
easterEggs_panic = "https://cdn.discordapp.com/attachments/307910914588540929/401832495307292682/6112012013224turningoffyourcellphonewhenitgoesoffinclass.gif"
easterEggs_hypeSquad = "https://cdn.discordapp.com/attachments/326736434763661312/419582034202198016/kedengmeme.gif"
easterEggs_snack = "I have type II diabetes, you know that I can't eat that, Liam."
easterEggs_frickLink = "https://media.discordapp.net/attachments/326736434763661312/485539223819255828/unknown.png"

#endregion

#endregion

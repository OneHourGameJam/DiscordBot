"""
ABOUT:
Stores custom variables the bot uses
"""
import SecretKeys

import os
directory_path = os.path.dirname(os.path.realpath(__file__))

# region DEBUG
DEBUG = True
DEBUG_channel = '394169935510896643'

DEBUG_modChannel = '307628493473054720'
# endregion

# region Enabling Features
usingLastTheme = True
usingRandomTheme = True
usingEasterEggs = True
usingTwitterBot = True
usingAutoTwitterBot = True
usingJamReminder = True
# endregion

# Server settings
adminRoleName = "moderator"

reminder_JamChannel = '307620502158049281'
# endregion

# region Secret keys
bot_key = SecretKeys.botKey  # The Discord bot key used in bot.run

# Keys used in tweetbot.py
twitter_consumerKey = SecretKeys.twitter_consumerKey
twitter_consumerSecret = SecretKeys.twitter_consumerSecret
twitter_accessToken = SecretKeys.twitter_accessToken
twitter_tokenSecret = SecretKeys.twitter_tokenSecret
# endregion

# region Twitter

# The minimum amount that needs to pass until a new tweet is allowed (in seconds)
twitter_timeSinceTweet = 28800  # Default: 28800 sec => 8 hours
twitter_hashtags = "#1hgj #gamedev #gamejam #indiedev #games"
# endregion

# region Server config
server_secretKey = SecretKeys.server_secretKey

server_changeLastTweetURL = "http://devillime.com/ohgj/bot/changelasttweet.php?"
server_displayLastTweetURL = "http://devillime.com/ohgj/bot/displaylasttweet.php"

server_randomThemeURL = "http://devillime.com/ohgj/bot/addtheme.php?"
server_displayThemeURL = "http://devillime.com/ohgj/bot/displaytheme.php"
# endregion

# region Dynamic Command Responses
commands_themeNotAnnounced = "The theme hasn't been announced yet."
commands_theme = "The theme is: \"{}\""
commands_getLastTheme = "The previous jam's theme was: '{}'"
commands_getTime_Upcoming = "{} left until the next jam."
commands_getTime_Ongoing = "{} left."
# endregion

# region One Hour Game Jam Links
links_API = "https://onehourgamejam.com/api/nextjam/"  # The link to the NextJam API

links_rules = "https://onehourgamejam.com/?page=rules"  # The link to the rules page
links_themes = "https://onehourgamejam.com/?page=themes"  # The link the the theme voting page
links_submit = "https://onehourgamejam.com/?page=submit"  # The link to the game submission page
links_login = "https://onehourgamejam.com/?page=login"  # The link to the log in/sign up page

links_GitHubIssues = "https://github.com/OneHourGameJam/OneHourGameJam-discord-bot/issues/"

links_Hyoe_Github = "https://github.com/OneHourGameJam/OneHourGameJam-discord-bot/issues/2"
# endregion

# region Static commands

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
        "!login" \
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
# endregion

# region Easter Eggs

easterEggs_hypeLinks = ["https://goo.gl/5TKpck", "https://youtu.be/gMkrvTraVZ0", "http://youtu.be/lSxh-UK7Ays",
"https://cdn.discordapp.com/attachments/326736434763661312/419582034202198016/kedengmeme.gif", "https://www.youtube.com/watch?v=zpGU355C0ak", "https://www.youtube.com/watch?v=s6E3xVz01bw", "https://www.youtube.com/watch?v=FDs6dADBmI0"]

easterEggs_panicLinks = ["https://tenor.com/view/emergency-animated-cartoon-spongebob-squarepants-siren-gif-6224023", "https://tenor.com/view/spongebob-patrick-panic-run-scream-gif-4655431", "https://tenor.com/view/please-gif-5054709", "https://tenor.com/view/kermit-scared-freakout-gif-5351805"

]

# endregion

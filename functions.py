import requests
import math
from random import randint

def getJamInfo(index : int):
    response = 'Response not set'

    apiURL = "http://onehourgamejam.com/api/nextjam/"
    page = requests.get(apiURL)
    content = page.content.decode('UTF-8')

    info = content.split("],")

    now = getNow(info[0])
    upcoming = info[0][29:]

    Info = { 0 : upcoming, 1 : info[1], 2 : info[2], 3 : now }
    # 0 Upcoming
    # 1 Current
    # 2 Previous
    # 3 now

    # THEME
    if(index == 0):
        if(isJamOn(Info[1])):
            response = "is " + getCurrentJam(Info[1], 1)
        else:
            response = "hasn't been announced yet."

    # TIME
    elif(index == 1):
        if(isJamOn(Info[1])):
            response = getTime(getCurrentJam(Info[1], 3), True) + " left."
        else:
            response = getTime(getUpcomingJam(Info[0], 3), False) + " left until the next jam."

    elif(index == 2):
        response = getLastJamTheme(Info[2])


    return response

def getUpcomingJamLong(index : int):
    response = 'Response not set'

    apiURL = "http://onehourgamejam.com/api/nextjam/"
    page = requests.get(apiURL)
    content = page.content.decode('UTF-8')

    info = content.split("],")

    now = getNow(info[0])
    upcoming = info[0][29:]

    Info = { 0 : upcoming, 1 : info[1], 2 : info[2], 3 : now }
    # 0 Upcoming
    # 1 Current
    # 2 Previous
    # 3 now

    string = Info[0]

    string = string[19:]
    string = string.replace("}", "")

    info = string.split(",")

    Info = {}
    i = 0

    for val in info:
        s = val.split("\":")
        S = s[1]

        Info[i] = S
        i += 1


    # 0 - - Jam number
    # 1 - - Theme
    # 2 - - Start Time
    # 3 - - Time difference

    return Info[index]


def getLastJamTheme(info : str):
    response = "getLastJamTheme"

    info = info.replace("\"previous_jams\":[{", "")
    info = info.replace("]}", "")

    infoSplit = info.split("},{")
    lastJam = infoSplit[infoSplit.__len__() - 1]

    lastJam = lastJam.replace("}", "")

    lastJamSplit = lastJam.split(",")

    theme = lastJamSplit[1]
    theme = theme.replace("\"theme\":\"", "")
    theme = theme.replace("\"", "")

    response = theme

    return response

def getUpcomingJam(string : str, index : int):
    string = string[19:]
    string = string.replace("}", "")

    info = string.split(",")

    Info = {}
    i = 0

    for val in info:
        s = val.split("\":")
        S = s[1]

        Info[i] = S
        i += 1

    print()

    # 0 - - Jam number
    # 1 - - Theme
    # 2 - - Start Time
    # 3 - - Time difference

    return Info[index]

def getCurrentJam(string : str, index : int):
    string = string[17:]
    string = string.replace("}", "")

    info = string.split(",")

    Info = {}
    i = 0

    for val in info:
        s = val.split("\":")
        S = s[1]

        Info[i] = S
        i += 1

    # 0 - - Jam number
    # 1 - - Theme
    # 2 - - Start Time
    # 3 - - Time difference

    return Info[index]

def getNow(string : str):
    array = string.split(",")

    now = array[0].replace("{\"now\":\"", "")
    now = now.replace("\"", "")

    return now;

def isJamOn(string : str):
    string = string[16:]
    if(string == ""):
        return False
    else:
        return True

def getTime(timeDiff : str, jamOn : bool):
    i = int(timeDiff)
    response = ""



    if(jamOn == False):
        i = abs(i)

        if (i / 60 < 1): # SEC
            response = i + " second" + plurality(i)

        if (i / 60 >= 1): # MIN
            minutes = int(math.floor(i / 60))
            response = str.format("{0} minute{1} ", minutes, plurality(minutes))

            sec = int(math.floor(i % 60))
            response += str.format("{0} second{1}", sec, plurality(sec))

        if (i / 3600 >= 1): # HOUR
            hours = int(math.floor((i / 3600)))
            response = str.format("{0} hour{1} ", hours, plurality(hours))

            minutes = int(math.floor((i % 3600) / 60))
            response += str.format("{0} minute{1}", minutes, plurality(minutes))

        if (i / 86400 >= 1): # DAY

            days = int(math.floor(i / 86400))

            response = str.format("{0} day{1} ", days, plurality(days))

            hours = int(math.floor((i % 86400) / 3600))
            response += str.format("{0} hour{1} ", hours, plurality(hours))

            minutes = int(math.floor(((i % 86400) % 3600) / 60))
            response += str.format("{0} minute{1}", minutes, plurality(minutes))

    else:
        i = 3600 + i

        if (i / 60 < 1): # SEC
            response = str.format("{0} second{1}", i, plurality(i))

        if (i / 60 >= 1): # MIN
            minutes = int(math.floor((i / 60)))
            response = str.format("{0} minute{1}", minutes, plurality(minutes))
            sec = int(math.floor(i % 60))
            response += str.format(" {0} second{1}", sec, plurality(sec))

    return response

def plurality(num : int):

    string = str(num)

    response = ""
    if (string == "1"):
        response = ""
    else:
        response = "s"

    return response

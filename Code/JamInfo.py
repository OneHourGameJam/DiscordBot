'''
ABOUT:
Contains functions that deal with the One Hour Game Jam API (http://onehourgamejam.com/api/nextjam/).
'''
import json
import requests
import datetime
from collections import namedtuple

import Config

#region JSON

'''
API JSON structure:
{
"now":"Y-M-D h:m:s",
"upcoming_jams":[
        {
        "number":INT,
        "theme":"Not announced yet",
        "start_datetime":"Y-M-D h:m:s",
        "timediff":INT  #(start_datetime - now (in seconds))
        }
    ],
"current_jams":[
        {
        "number":INT,
        "theme":STRING,
        "start_datetime":"Y-M-D h:m:s",
        "timediff":INT  #(start_datetime - now (in seconds))
        }
    ],
"previous_jams":[
        {
        "number":INT,
        "theme":STRING,
        "start_datetime":"%Y-%m-%d %H:%M:%S",
        "timediff":INT  #(start_datetime - now (in seconds))
        }
    ]
}
'''

Jam = namedtuple('Jam', 'number, theme, start_datetime, timediff') # Create a named tuple for the JSON jam format

#endregion

def __getInfo():
    r"""Returns the JSON string from the One Hour Game Jam API
    """

    apiURL = Config.links_API # The url with the JSON string
    page = requests.get(apiURL) # Get the content of the API page

    content = page.content.decode('UTF-8') # Decode the page content with UTF-8

    return json.loads(content) # Return the string in a JSON-friendly format

def getNow():
    r"""Gets the server time from the One Hour Game Jam API
    The server time should be UTC
    :return: datetime
    """
    info = __getInfo() # Get the JSON string from the API page
    nowSTR = info['now'] # Get the string of 'now'

    nowDT = datetime.datetime.strptime(nowSTR, "%Y-%m-%d %H:%M:%S") # Convert the JSON string into a datetime object

    return nowDT

def getCurrentTheme():
    r"""Gets the theme of the ongoing jam.
    If there is no ongoing jam it returns an empty string
    :return: str
    """
    info = __getInfo() # Get the JSON string from the API page
    currentJams = info['current_jams'] # Get the 'current_jams' array

    if(ongoingJam(currentJams) == False): # If the array's length is 0 that means there is no ongoing jam
        return "" # Return an empty string to indicate that there isn't an ongoing jam

    jams = [Jam(**k) for k in currentJams]
    theme = jams[0].theme # Get the theme from the ongoing jam (there should only be one jam in this array)

    return theme #return the theme

def getLastTheme():
    r"""
    Gets the theme of the previous jam
    :return: str
    """
    info = __getInfo() # Get the JSON string from the API page
    previousJams = info['previous_jams'] # Get the 'previous_jams' array

    jams = [Jam(**k) for k in previousJams] # Get an array of jams in 'previous_jams' (Jam is a named tuple -- see above in region "JSON")

    previousTheme = jams[jams.__len__() - 1].theme # Get the theme from the last jam in the array

    return previousTheme

def ongoingJam(currentJams : list = None):
    r"""Is there an ongoing jam?
    
    :param currentJams: The JSON string or 'current_jams'
    :return: bool
    """
    if(currentJams == None):
        info = __getInfo()  # Get the JSON string from the API page
        currentJams = info['current_jams']  # Get the 'current_jams' array

    if(currentJams.__len__() == 0): # If the array is empty (length = 0) that means there is no ongoing jam
        return False
    else:
        return True

def getTimeDiff():
    r"""Gets the time remaining to either the end of the ongoing jam or the next jam
    :return: time
    """
    info = __getInfo() # Get the JSON string from the API
    currentJams = info['current_jams'] # Get the array of current jams
    jams = []
    if(ongoingJam(currentJams)): # If there's an ongoing jam we want to get that one's data
        jams = [Jam(**k) for k in currentJams] # Get an array of jams in 'current_jams' (Jam is a named tuple -- see above in region "JSON")

    else: # If there isn't an ongoing jam return the time left until the next one
        upcomingJams = info['upcoming_jams'] # Get the array of the upcomingJams
        jams = [Jam(**k) for k in upcomingJams] # Get an array of jams in 'upcoming_jams' (Jam is a named tuple -- see above in region "JSON")

    return jams[0].timediff  # Return the timediff

def formatTime(timeDiff : int):
    r"""Returns a formatted time diff
    :param timeDiff: Time left until the jam (should always be positive)
    :return: str[]
    """
    if(timeDiff < 0): # timeDiff should never be negative in this function
        return "ERROR: Negative timeDiff"

    response = ["", "", "", ""] # Create an array of formatted times (DAYS HOURS MINUTES SECONDS)

    # Convert from seconds into days, hours, minutes and seconds
    m, s = divmod(timeDiff, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)

    if(d == 1): response[0] = "1 day"
    elif(d > 1): response[0] = "{} days".format(d)

    if (h == 1): response[1] = "1 hour"
    elif (h > 1): response[1] = "{} hours".format(h)

    if (m == 1): response[2] = "1 minute"
    elif (m > 1): response[2] = "{} minutes".format(m)

    if (s == 0): response[3] = "0 seconds"
    elif (s == 1): response[3] = "1 second"
    elif (s > 1): response[3] = "{} seconds".format(s)

    return response

def getUpcomingJamDate():
    r"""Gets the date of the upcoming jam
    :return: datetime
    """
    info = __getInfo() # Get the JSON string from the API
    upcomingJams = info['upcoming_jams'] # Get the array of the upcomingJams
    jams = [Jam(**k) for k in upcomingJams] # Get an array of jams in 'upcoming_jams' (Jam is a named tuple -- see above in region "JSON")

    return datetime.datetime.strptime(jams[0].start_datetime, "%Y-%m-%d %H:%M:%S")  # Return the datetime

def getCurrentJamNumber():
    r"""
    :return: str
    """
    info = __getInfo()
    currentJams = info['current_jams']
    jams = [Jam(**k) for k in currentJams]

    return jams[0].number
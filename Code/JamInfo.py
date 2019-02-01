"""
Contains functions that deal with the One Hour Game Jam API (http://onehourgamejam.com/api/nextjam/).
"""
import json
import requests
import datetime
from collections import namedtuple

import Config

# region JSON

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

# endregion

Jam = namedtuple('Jam', 'number, theme, start_datetime, timediff')  # Create a named tuple for the JSON jam format


def __getInfo():
    r"""Returns the JSON string from the One Hour Game Jam API
    """

    api_url = Config.links_API  # The url with the JSON string
    page = requests.get(api_url)  # Get the content of the API page

    content = page.content.decode('UTF-8')  # Decode the page content with UTF-8

    return json.loads(content)  # Return the string in a JSON-friendly format


def getNow():
    r"""Gets the server time from the One Hour Game Jam API
    The server time should be UTC
    :return: datetime
    """
    info = __getInfo()  # Get the JSON string from the API page
    now_str = info['now']  # Get the string of 'now'

    now_dt = datetime.datetime.strptime(now_str, "%Y-%m-%d %H:%M:%S")  # Convert the JSON string into a datetime object

    return now_dt


def getCurrentTheme():
    r"""Gets the theme of the ongoing jam.
    If there is no ongoing jam it returns an empty string
    :return: str
    """
    info = __getInfo()
    current_jams = info['current_jams']

    if not ongoingJam(current_jams):  # If the array's length is 0 that means there is no ongoing jam
        return ""

    jams = [Jam(**k) for k in current_jams]

    return jams[0].theme


def getLastTheme():
    r"""
    Gets the theme of the previous jam
    :return: str
    """
    info = __getInfo()
    previous_jams = info['previous_jams']

    jams = [Jam(**k) for k in previous_jams]

    previous_theme = jams[jams.__len__() - 1].theme  # Get the theme from the last jam in the array

    return previous_theme


def ongoingJam(current_jams: list = None):
    r"""Is there an ongoing jam?
    
    :param current_jams: The JSON string or 'current_jams'
    :return: bool
    """
    if current_jams is None:
        info = __getInfo()
        current_jams = info['current_jams']

    if current_jams.__len__() == 0:  # If the array is empty that means there is no ongoing jam
        return False
    else:
        return True


def getTimeDiff():
    r"""Gets the time remaining to either the end of the ongoing jam or the next jam
    :return: time
    """
    info = __getInfo()
    current_jams = info['current_jams']

    if ongoingJam(current_jams):  # If there's an ongoing jam we want to get that one's data
        jams = [Jam(**k) for k in current_jams]

    else:  # If there isn't an ongoing jam return the time left until the next one
        upcoming_jams = info['upcoming_jams']
        jams = [Jam(**k) for k in upcoming_jams]

    return jams[0].timediff


def formatTime(time_diff: int):
    r"""Returns a formatted time diff
    :param time_diff: Time left until the jam (should always be positive)
    :return: str[]
    """
    if time_diff < 0:  # timeDiff should never be negative in this function
        return "ERROR: Negative timeDiff"

    response = ["", "", "", ""]  # Create an array of formatted times (DAYS HOURS MINUTES SECONDS)

    # Convert from seconds into days, hours, minutes and seconds
    m, s = divmod(time_diff, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)

    if d == 1: response[0] = "1 day"
    elif d > 1: response[0] = "{} days".format(d)

    if h == 1: response[1] = "1 hour"
    elif h > 1: response[1] = "{} hours".format(h)

    if m == 1: response[2] = "1 minute"
    elif m > 1: response[2] = "{} minutes".format(m)

    if s == 0: response[3] = "0 seconds"
    elif s == 1: response[3] = "1 second"
    elif s > 1: response[3] = "{} seconds".format(s)

    return response


def getUpcomingJamDate():
    r"""Gets the date of the upcoming jam
    :return: datetime
    """
    info = __getInfo()
    upcoming_jams = info['upcoming_jams']
    jams = [Jam(**k) for k in upcoming_jams]

    return datetime.datetime.strptime(jams[0].start_datetime, "%Y-%m-%d %H:%M:%S")  # Return the datetime


def getCurrentJamNumber():
    r"""
    :return: str
    """
    info = __getInfo()
    current_jams = info['current_jams']
    jams = [Jam(**k) for k in current_jams]

    return jams[0].number
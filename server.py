import _md5
import requests
from datetime import datetime

import Config

def generateHash(key : str):
    string = key + Config.server_secretKey
    string = string.encode('utf-8')

    return _md5.md5(string).hexdigest()

def addRandomTheme(name : str, hash : str):
    url = Config.server_randomThemeURL + "name=" + name + "&hash=" + hash

    requests.get(url)

def getRandomTheme():
    page = requests.get(Config.server_displayThemeURL)
    content = page.content.decode('UTF-8')

    return content

def getLastTweet():
    page = requests.get(Config.server_displayLastTweetURL)
    content = page.content.decode('UTF-8')

    return datetime.strptime(content.replace("_", " "), "%Y-%m-%d %H:%M:%S")

def changeLastTweet():
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S").replace(" ", "_")
    previous = getLastTweet().strftime("%Y-%m-%d %H:%M:%S").replace(" ", "_")

    url = Config.server_changeLastTweetURL + "timestamp=" + now + "&hash=" + generateHash(now) + "&lasttimestamp=" + previous

    requests.get(url)
import _md5
import requests
from datetime import datetime

changeLastTweetURL = "http://devillime.com/ohgj/bot/changelasttweet.php?"
randomThemeURL = "http://devillime.com/ohgj/bot/addtheme.php?"
secretKey = "INSERT SECRET KEY"



def generateHash(key : str):
    string = key + secretKey
    string = string.encode('utf-8')

    return _md5.md5(string).hexdigest()

def addRandomTheme(name : str, hash : str):
    url = randomThemeURL + "name=" + name + "&hash=" + hash

    requests.get(url)

def checkBlacklist(string : str):
    #blacklist = open("blacklist.txt", 'r')
    #blacklist = open("/usr/local/lib/python3.5/dist-packages/ohgj_discord-bot/blacklist.txt", 'r')
    blacklist = open("/usr/local/lib/python3.5/dist-packages/ohgj_discord-bot/test.txt", 'r')
    content = blacklist.read()

    words = content.split("\n")

    for word in words:
        if(string.__contains__(word)):
            return True

    return False

def getRandomTheme():
    URL = "http://devillime.com/ohgj/bot/displaytheme.php"
    page = requests.get(URL)
    content = page.content.decode('UTF-8')

    return content

def getLastTweet():
    URL = "http://devillime.com/ohgj/bot/displaylasttweet.php"
    page = requests.get(URL)
    content = page.content.decode('UTF-8')

    return datetime.strptime(content.replace("_", " "), "%Y-%m-%d %H:%M:%S")

def changeLastTweet():
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S").replace(" ", "_")
    previous = getLastTweet().strftime("%Y-%m-%d %H:%M:%S").replace(" ", "_")

    url = changeLastTweetURL + "timestamp=" + now + "&hash=" + generateHash(now) + "&lasttimestamp=" + previous
    #print(url)

    requests.get(url)
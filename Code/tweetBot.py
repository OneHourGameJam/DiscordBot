import tweepy
import Config
import server


def __get_api(cfg):
    auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
    auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
    return tweepy.API(auth)


def tweet(contents: str):
    r"""Tweets via the Twitter bot API
    :param contents: The contents of the tweet
    :return: Returns a string containing the result
    """
    cfg = {
        "consumer_key": Config.twitter_consumerKey,
        "consumer_secret": Config.twitter_consumerSecret,
        "access_token": Config.twitter_accessToken,
        "access_token_secret": Config.twitter_tokenSecret
    }

    api = __get_api(cfg)
    if contents.count(contents) <= 280:  # Check if the string is small enough to fit into a single tweet
        api.update_status(status=contents)
        server.changeLastTweet()  # Change the timestamp of the last tweet
        return "Tweet sent"

    else:
        print("Too many characters to tweet: " + contents.count(contents).__str__())
        return "Tweet error: Too many characters to tweet"

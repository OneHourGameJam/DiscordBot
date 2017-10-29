import tweepy


def get_api(cfg):
  auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
  auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
  return tweepy.API(auth)

def tweet(contents : str):
  cfg = {
    "consumer_key"        : "",
    "consumer_secret"     : "",
    "access_token"        : "",
    "access_token_secret" : ""
    }

  api = get_api(cfg)
  if(contents.count(contents) <= 140):
    status = api.update_status(status=contents)
    return "Tweet sent"
  else:
      print("Too many characters to tweet!")
      return "Tweet error: Too many characters to tweet"



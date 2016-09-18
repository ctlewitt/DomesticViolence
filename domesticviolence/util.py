import re
import twitter

HEADLINE = 0
AUTHOR = 1
CONTENT = 2
ARTICLE_URL = 3
MEDIA_PROVIDER = 4
PUBLISH_DATE = 5
FOLLOWING = 6
FOLLOWERS = 7
UPDATES = 8
BLOG_POST_SENTIMENT = 9
ARTICLE_ID = 10


# checks if a post is possibly relevant:
# returns True if post is from Twitter, not a retweet, and does not include the words
# "hashtag, read, important, trending, sparked, article, stream"


def relevant_tweet(tweet_parts):
    # check if from twitter
    if not post_is_tweet(tweet_parts):
        return False
    # check if RT
    if post_is_retweet(tweet_parts):
        return False
    # check if _about_ WhyIStayed/WhyILeft, instead of from victim
    if post_contains_commentary(tweet_parts):
        return False
    if post_contains_link(tweet_parts):
        return False
    return True


# returns False if post is not from Twitter; True if it is
def post_is_tweet(tweet_parts):
    if tweet_parts[MEDIA_PROVIDER] == "TWITTER":
        return True
    return False


# return True if post is a retweet, False otherwise
def post_is_retweet(tweet_parts):
    if re.match(r'("?RT @)', tweet_parts[CONTENT]) is not None:
        return True
    return False


# returns True if post contains commentary language
# (e.g., "hashtag, read, important, trending, sparked, article, stream")
def post_contains_commentary(tweet_parts):
    regex1 = re.compile(r"hashtag|thread|infographic|\bread\b|powerful tweets|check out|enlightening|everyone needs to see"
                        r"|real people|thanks for sharing|stories being shared|must see|justice system|god bless|abc news")
    regex2 = re.compile(r"important|insightful|reading|\breads\b|open up|real issues|trending|sparked|article|stream|movement")
    if regex1.search(tweet_parts[CONTENT].lower()) is not None or regex2.search(tweet_parts[CONTENT].lower()) is not None:
        return True
    return False


def post_contains_commentary2(tweet_parts):
    regex1 = re.compile(r"pizza|bacon|article|have you heard|campaign|political|twitter|heartbreaking|heartbreak|why they stay|congress|broadening views")
    regex2 = re.compile(r"discussion on|catching up with|@huffingtonpost|ray rice|posting|social media|series|now taking your questions|r u serious")
    regex3 = re.compile(r"eye opening|recommend|checking out|still don't get it|corageous|take a look at|article|dialogue|reporter|my feed\b|news feed\b")
    if (regex1.search(tweet_parts[CONTENT].lower()) is not None
        or regex2.search(tweet_parts[CONTENT].lower()) is not None
        or regex3.search(tweet_parts[CONTENT].lower()) is not None):
        return True
    return False


def post_contains_link(tweet_parts):
    if re.search(r'(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))', tweet_parts[CONTENT]) is not None:
        return True
    return False


def get_tweet_parts(line):
    tweet_parts = line.strip().split(",")
    num_tweet_parts = len(tweet_parts)
    if num_tweet_parts > 11:
        num_extra_tweets_parts = num_tweet_parts - 11 + 1
        tweet_parts = tweet_parts[:2] + [",".join(tweet_parts[2:2+num_extra_tweets_parts])] + tweet_parts[2+num_extra_tweets_parts:]
    return tweet_parts


def get_num_lines(file):
    num_lines = 0
    with open(file, "r") as r_file:
        for line in r_file:
            num_lines += 1
    return num_lines


# function to initialize and return twitter api connection
def connect_twitter_api():
    # user credentials to access Twitter API
    ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
    ACCESS_SECRET = os.environ.get('ACCESS_SECRET')
    CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
    CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')

    # create Api instance
    api = twitter.Api(consumer_key=CONSUMER_KEY,
                      consumer_secret=CONSUMER_SECRET,
                      access_token_key=ACCESS_TOKEN,
                      access_token_secret=ACCESS_SECRET,
                      sleep_on_rate_limit=True)

    return api

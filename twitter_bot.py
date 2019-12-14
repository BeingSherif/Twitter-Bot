from twython import Twython, TwythonStreamer, TwythonError
import time
from pathlib import Path
import schedule 


def twitter_api():

    """ Authenticate credentials"""
    # Replace the placeholder below with your credentials
    CONSUMER_KEY = "YOUR CONSUMER KEY HERE"
    CONSUMER_SECRET = "YOUR CONSUMER SECRET KEY HERE"
    ACCESS_TOKEN = "YOUR ACCESS TOKEN HERE"
    ACCESS_TOKEN_SECRET = "YOUR ACCESS TOKEN HERE"
    twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return twitter


def save_last_tweet_id(tweet_id):
    """ We are using this function to store the tweet ids we've already processed"""
    with open("last_tweet_ids.txt", "a") as file:
        file.write(str(tweet_id) + "\n")
        print("Tweet id saved!")

def get_last_tweet_ids():
    """ Fetch tweet ids """
    # create the text file if it doesn't exist
    filename = Path('last_tweet_ids.txt')
    filename.touch(exist_ok=True)
    with open("last_tweet_ids.txt", "r") as file:
        tweet_ids = [ids.strip() for ids in file.readlines()]
    return tweet_ids


def like_and_retweet():

    api = twitter_api()
    # Getting 10 recent mentioned tweets 
    recent_tweets_object = api.get_mentions_timeline(count=10)[:2]
    last_tweet_ids = get_last_tweet_ids()
    # we iterate over the most recent tweets object
    for tweet in recent_tweets_object:
        tweet_id = tweet.get("id_str")
        # we want to check if we already retweet and like the tweet.
        if tweet_id not in last_tweet_ids:
            try:
                # Here we are retweeting the tweet using the tweet id
                api.retweet(id=tweet_id)
                print("Tweet retweeted")
                # sleeping for some seconds between retweet and liking the tweet
                time.sleep(3)
                # here we are favoriting the tweet
                api.create_favorite(id=tweet_id)
                print("Tweet favorited!")
                # save the tweet id to the last_tweet_ids.txt
                save_last_tweet_id(tweet_id)
                print(f"Tweet id {tweet_id} saved")

            except TwythonError as e:
                print(e)
        else:
            print(f"Already retweet and like tweet with the id {tweet_id}")

# we are using this to schedule and check for new mentions every hour
schedule.every().hour.do(like_and_retweet)

if __name__ == "__main__":
    print("[+] Check for new mentions every hour...")
    while True:
        schedule.run_pending()
        time.sleep(1)
   
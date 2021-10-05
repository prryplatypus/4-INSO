import json

from os import getenv

import tweepy


class TweetStream(tweepy.Stream):
    def on_data(self, data):
        json.loads(data)

    def on_exception(self, exception):
        return super().on_exception(exception)

stream = TweetStream(
    getenv('CONSUMER_KEY'),
    getenv('CONSUMER_SECRET'),
    getenv('ACCESS_TOKEN'),
    getenv('ACCESS_TOKEN_SECRET'),
)

stream.filter(track=["La Palma"])

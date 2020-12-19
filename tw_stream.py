#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from os import path

import configparser
import twitter

from cmc import get_twitter_names
from tele_client import handle_message
from utils import chunker

config = configparser.ConfigParser()
config.read("twit_config.ini")

consumer_key = config['Twitter']['consumer_key']
consumer_secret = config['Twitter']['consumer_secret']
access_token_key = config['Twitter']['access_token_key']
access_token_secret = config['Twitter']['access_token_secret']

api = twitter.Api(consumer_key=consumer_key,
                  consumer_secret=consumer_secret,
                  access_token_key=access_token_key,
                  access_token_secret=access_token_secret)


def write_to_file(ids):
    f = open("twitter_ids.txt", "a+")
    for o in ids:
        f.write('%s\n' % o)
    f.close()


def get_follow_ids(twitter_names):
    ids = []
    if path.exists("twitter_ids.txt"):
        f = open("twitter_ids.txt", "r+")
        for line in f:
            c = line[:-1]
            ids.append(c)
        f.close()
        return ids
    else:
        for t in list(chunker(twitter_names, 100)):
            follow_ids = []
            for user in api.UsersLookup(screen_name=t):
                id_str = json.loads(user.__str__())['id_str']
                follow_ids.append(id_str)
            write_to_file(follow_ids)


twitter_names = get_twitter_names()
ids_to_follow = get_follow_ids(twitter_names)
track = []

stream = api.GetStreamFilter(follow=ids_to_follow, track=track, filter_level=None)
while stream:
    msg = stream.__next__()
    if 'extended_tweet' in msg.keys():
        tweet = "\n\n\n=> TWEET: " + msg['extended_tweet']['full_text'] + "\n FROM: " + msg['user']['screen_name']
        if ids_to_follow.__contains__(msg['user']['id_str']):
            print(tweet)
            # handle_message(tweet)
#
# if __name__ == "__main__":
#     t_names = get_twitter_names()
#     print (get_follow_ids(t_names))

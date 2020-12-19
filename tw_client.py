#!/usr/bin/env python3

import configparser
import twitter

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

print(api.VerifyCredentials())


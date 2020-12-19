#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import requests
import configparser

config = configparser.ConfigParser()
config.read("tele_config.ini")

channel = config['Telegram']['channel']
bot_token = config['Telegram']['bot_token']

def send_text(bot_message):

    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=-348399438&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()
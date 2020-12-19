#!/usr/bin/env python3

import configparser

from telethon import TelegramClient

config = configparser.ConfigParser()
config.read("tele_config.ini")

api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']

api_hash = str(api_hash)

channel = config['Telegram']['channel']
bot_token = config['Telegram']['bot_token']

client = TelegramClient('crypt_007_bot', api_id, api_hash).start(bot_token= bot_token)
print("Client Created")

async def send_message(message):
    await client.send_message(-348399438, message= message)

def handle_message(message):
    with client:
        client.loop.run_until_complete(send_message(message))

import random
import discord
import giphy_client
from giphy_client.rest import ApiException
import os
import asyncio
from dotenv import load_dotenv, find_dotenv
load_dotenv()

discord_token = os.environ['your_discord_bot_token']
giphy_token = os.environ['your_giphy_api_key']

api_instance = giphy_client.DefaultApi()


def search_gifs(query):
    try:
        return api_instance.gifs_search_get(giphy_token, query,
                                            limit=5, rating='g')

    except ApiException as e:
        return "Exception when calling DefaultApi->gifs_search_get: %s\n" % e


def gif_response(emotion):
    try:
        gifs = search_gifs(emotion)
        lst = list(gifs.data)
        gif = random.choices(lst)

        return gif[0].url
    except IndexError:
        return "Cannot find anything similar. Try better!"

class DiscordClient(discord.Client):
    async def on_ready(self):
        print("Login as")
        print(self.user)
        print("-------")
    async def on_message(self, message):
        # Whenever a user other than bot says "hi"
        if message.author != self.user:
            if "!gif " in message.content:
                await message.channel.send(message.author.mention + ' say ' + message.content)
                await message.channel.send(gif_response(message.content.replace("!gif ", "")))
            elif message.content == 'hi':
                await message.channel.send('Hi there!!! ' + message.author.mention)
                await message.channel.send(gif_response('hi'))

            elif message.content == 'hello':
                await message.channel.send('Hello :) ' + message.author.mention)
                await message.channel.send(gif_response('hello'))
            elif message.content == 'welcome':
                await message.channel.send(message.author.mention +
                    ' Welcome to the discord channel :)')
                await message.channel.send(gif_response('welcome'))
            elif message.content == 'bye':
                await message.channel.send(message.author.mention +
                    ' May the force be with you')
                await message.channel.send(gif_response('star wars bye'))

            elif message.content == "good bye":
                await message.channel.send(message.author.mention +
                    ' Live long and prosper')
                await message.channel.send(gif_response('salute'))


client = DiscordClient()
client.run(discord_token)

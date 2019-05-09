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
                                            limit=5, rating='r',
                                            lang=["en","ru","ua"]
                                               )

    except ApiException as e:
        return "Exception when calling DefaultApi->gifs_search_get: %s\n" % e

def translate_gifs(query):
    try:
        return api_instance.gifs_translate_get(giphy_token, query)

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

def gif_translate_response(emotion):
    try:
        gifs = translate_gifs(emotion)
        return gifs.data.url
    except IndexError:
        return "Cannot find anything similar. Try better!"

def translate_stickers(query):
    try:
        return api_instance.stickers_translate_get(giphy_token, query)

    except ApiException as e:
        return "Exception when calling DefaultApi->gifs_search_get: %s\n" % e

def sticker_translate_response(emotion):
    try:
        gifs = translate_stickers(emotion)
        return gifs.data.url
    except IndexError:
        return "Cannot find anything similar. Try better!"

def search_stickers(query):
    try:
        return api_instance.stickers_search_get(giphy_token, query,
                                            limit=5, rating='r',
                                            lang=["en","ru","ua"])

    except ApiException as e:
        return "Exception when calling DefaultApi->stickers_search_get: %s\n" % e

def sticker_response(emotion):
    try:
        stickers = search_stickers(emotion)
        lst = list(stickers.data)
        sticker = random.choices(lst)

        return sticker[0].url
    except IndexError:
        return "Cannot find anything similar. Try better!"

class DiscordClient(discord.Client):
    async def on_ready(self):
        print("Login as")
        print(self.user)
        print("-------")
        await self.change_presence(activity=discord.Game(name="World of Warcraft"), status=discord.Status.online)
        # server = self.get_server("264384440627625984")
        '''
        server = discord.utils.get(self.guilds)
        print(server)

        role = discord.utils.get(server.roles)
        print(role)
        members = discord.utils.get(server.members)
        print(members.name)
        user = members.name
        print(discord.__version__) # Rewrite branch

        # role = discord.utils.get(user.server.roles, name="role to add name")
        await self.add_roles(user, role, hoist=True, colour=discord.Colour(0xe91e63))
        # client = discord.Client()
        await self.edit_role(server=server, role=role, hoist=True, colour=discord.Colour(0xe91e63))
        if server:
            for member in server.members:
                print('name: {}'.format(member.name) )
            else:
                print('any')
        '''
        # discord.ActivityType = 'playing'
        # discord.Colour(0xe91e63)

    async def on_message(self, message):
        # Whenever a user other than bot says "hi"
        if message.author != self.user:
            if "!gif " in message.content:
                await message.channel.send(message.author.mention + ' say ' + message.content)
                await message.channel.send(gif_response(message.content.replace("!gif ", "")))
            elif "!tgif " in message.content:
                await message.channel.send(message.author.mention + ' say ' + message.content)
                await message.channel.send(gif_translate_response(message.content.replace("!tgif ", "")))
            elif "!sticker " in message.content:
                await message.channel.send(message.author.mention + ' say ' + message.content)
                await message.channel.send(sticker_response(message.content.replace("!sticker ", "")))
            elif "!tsticker " in message.content:
                await message.channel.send(message.author.mention + ' say ' + message.content)
                await message.channel.send(sticker_translate_response(message.content.replace("!tsticker ", "")))

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

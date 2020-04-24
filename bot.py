# -*- coding: utf-8 -*-
import discord
from chuck import ChuckNorris

cn = ChuckNorris()
import os
import random

from utils import remove_accents
from secrets import DISCORD_TOKEN
from loquendo_api_tss import loquendo_interact
from reddit import reddit_interact
from meme_api import  meme_interact
from giphy_api import giphy_interact
from genius_api import genius_interact
class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
    async def on_message(self, message):
      print('Message from {0.author}'.format(message))
      #content = message.content.encode('ascii', 'ignore').decode('ascii')
      content = remove_accents(message.content)
      print('Message {0}'.format(content.encode('utf-8')))
      channel = message.channel
      if message.author.bot == False:
            if message.content.lower() == "help":
                  await channel.send('Available commands: -chuck norris -say x -yo mama')
            if message.content.lower() == "chuck norris":
                  await channel.send('A chuck norris joke is coming for you!')
                  # Get random jokes.
                  data = cn.random()
                  await channel.send(data)
            if message.content.lower() == "yo mama":
                  await channel.send("I'll send a yo mama joke")
                  with open("jokes.txt",'r',encoding = 'utf-8') as f:
                        lines = f.readlines()
                        await channel.send(random.choice(lines))
            if message.content.split()[0].lower() == "say":
                  await loquendo_interact(content,channel,False)
            if message.content.split()[0].lower() == "reddit":
                  await reddit_interact(content,channel)
            if message.content.split()[0].lower() == "meme":
                  await meme_interact(content,channel)
            if message.content.split()[0].lower() == "gif":
                  await giphy_interact(content,channel)
            if message.content.split()[0].lower() == "genius":
                  await genius_interact(content,channel,message.author,client)
      else:
            print("bot can't send messages as a user")
client = MyClient()
client.run(DISCORD_TOKEN)

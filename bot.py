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
from discord.ext import commands
bot = commands.Bot(command_prefix='', description='A bot that greets the user back.')

@bot.command()
async def greet(ctx):
      await ctx.send(":smiley: :wave: Hello, there!")
@bot.command()
async def chucknorris(ctx):
      await ctx.send('A chuck norris joke is coming for you!')
      # Get random jokes.
      data = cn.random()
      await ctx.send(data)
@bot.command()
async def yomama(ctx):
      await ctx.send("I'll send a yo mama joke")
      with open("jokes.txt",'r',encoding = 'utf-8') as f:
            lines = f.readlines()
            await ctx.send(random.choice(lines))
@bot.command()
async def say(ctx, arg1):
      await loquendo_interact(arg1,ctx.message.channel,False)
@bot.command()
async def reddit(ctx,*args):
      await reddit_interact(ctx.message.channel,args)
@bot.command()
async def meme(ctx,*args):
      await meme_interact(args,ctx.message.channel)
@bot.command()
async def gif(ctx,*args):
      await giphy_interact(args,ctx.message.channel)
@bot.command()
async def genius(ctx,*args):
      await genius_interact(args,ctx.message.channel,ctx.message.author,client)

@bot.event
async def on_ready():
      print("Bot is ready")
@bot.event
async def on_message(self, message):
      print('Message from {0.author}'.format(message))

bot.run(DISCORD_TOKEN)

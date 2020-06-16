# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from discord.ext.commands import CommandNotFound
from discord import FFmpegPCMAudio
from chuck import ChuckNorris

cn = ChuckNorris()


from utils import remove_accents
from secrets import DISCORD_TOKEN
from loquendo_api_tss import loquendo_interact
from reddit import reddit_interact
from meme_api import  meme_interact
from giphy_api import giphy_interact
from genius_api import genius_interact
from wikipedia_api import wikipedia_interact
from youtube_api import youtube_interact
from youtube_cutter_api import youtube_cutter_interact
# from tiktok_api import tiktok_interact


import os
import random
import gtts
import glob


soundnames = glob.glob("sonidos/*.mp3")
videonames = glob.glob("videos/*.mp4")
per = 30
rate = 3

bot = commands.Bot(command_prefix='-', description='La navaja suiza de los bots.')

@bot.command()
async def greet(ctx):
      await ctx.send(":smiley: :wave: Hello, there!")
@bot.command()
async def chucknorris(ctx):
      print("chucknorris called")
      await ctx.send('A chuck norris joke is coming for you!')
      # Get random jokes.
      data = cn.random()
      await ctx.send(data)
@bot.command()
async def yomama(ctx):
      print("yomama called")
      await ctx.send("I'll send a yo mama joke")
      with open("jokes.txt",'r',encoding = 'utf-8') as f:
            lines = f.readlines()
            await ctx.send(random.choice(lines))


@bot.command(pass_context=True)
@commands.cooldown(rate,per,BucketType.member) 
async def say(ctx, *args):
      print("say called")
      async with ctx.typing():
            await loquendo_interact(args,bot,ctx,ctx.message.channel,False)

@say.error
async def say_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'Vas muy rapido fiera,por favor espera {:.2f}s y no me jodas el puto server!'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error   

@say.before_invoke
async def ensure_voice(ctx):
	if ctx.voice_client is None:
		if ctx.author.voice:
			await ctx.author.voice.channel.connect()
		else:
			await ctx.send("You are not connected to a voice channel.")
			raise commands.CommandError("Author not connected to a voice channel.")
	elif ctx.voice_client.is_playing():
		ctx.voice_client.stop()
@bot.command()
async def reddit(ctx,*args):
      print("reddit called")
      await reddit_interact(ctx.message.channel,args)

@bot.command()
@commands.cooldown(rate,per,BucketType.member) 
async def meme(ctx,*args):
      print("meme called")
      await meme_interact(args,ctx.message.channel)
@meme.error
async def meme_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'Vas muy rapido fiera,por favor espera {:.2f}s y no me jodas el puto server!'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error  

@bot.command()
async def gif(ctx,*args):
      print("gif called")
      await giphy_interact(args,ctx.message.channel)
@bot.command()
async def genius(ctx,*args):
      print("genius called")
      await genius_interact(args,ctx.message.channel,ctx.message.author,bot)

@bot.command(pass_context=True)
async def youtubecutter(ctx,*args):
      print("Yputube caller called")
      await youtube_cutter_interact(args,ctx,bot)
      await reloadmemesound(ctx)
@youtubecutter.before_invoke
async def ensure_voice(ctx):
	if ctx.voice_client is None:
		if ctx.author.voice:
			await ctx.author.voice.channel.connect()
		else:
			await ctx.send("You are not connected to a voice channel.")
			raise commands.CommandError("Author not connected to a voice channel.")
	elif ctx.voice_client.is_playing():
		ctx.voice_client.stop()
@bot.command(pass_context=True)
async def yt(ctx,*args):
      print("YT called")
      async with ctx.typing():
            await youtube_interact(args,ctx,bot)

@bot.command(pass_context=True)
async def join(ctx):
	print("join")
	channel = ctx.message.author.voice.channel
	await channel.connect()

@bot.command(pass_context=True)
async def leave(ctx):
	print("leave")
	channel = ctx.message.author.voice.channel
	await ctx.voice_client.disconnect()


@yt.before_invoke
async def ensure_voice(ctx):
	if ctx.voice_client is None:
		if ctx.author.voice:
			await ctx.author.voice.channel.connect()
		else:
			await ctx.send("You are not connected to a voice channel.")
			raise commands.CommandError("Author not connected to a voice channel.")
	elif ctx.voice_client.is_playing():
		ctx.voice_client.stop()

@bot.command(pass_context=True)
async def volume(ctx, volume: int):
	if ctx.voice_client is None:
		return await ctx.send("Kein Audiochannel gefunden")
	ctx.voice_client.source.volume = volume / 100
	await ctx.send("Changed volume to {}".format(volume))
@bot.command()
async def reloadmemesound(ctx):
      global soundnames
      await ctx.message.channel.send("Getting new meme sounds.")
      size = len(soundnames)
      soundnames = glob.glob("sonidos/*.mp3")
      newsize = len(soundnames) - size
      await ctx.message.channel.send("Added {0} new meme sounds.".format(newsize))

@bot.command()
async def memesound(ctx,*args):
      print("memesound called")
      global soundnames
      print (soundnames)
      found = False
      if len(args) == 0:
            path = random.choice(soundnames)
            await ctx.send(file = discord.File(path))
            if not ctx.voice_client.is_playing():
                  ctx.voice_client.play(discord.FFmpegPCMAudio(path), after=lambda e: print('done', e))
            while not ctx.voice_client.is_done():
                  await asyncio.sleep(1)
            await ctx.voice_client.disconnect()
            found = True
      else:
            for name in soundnames:
                  if args[0] in name:
                        print("Sound found")
                        await ctx.send(file = discord.File(name))
                        if not ctx.voice_client.is_playing():
                              ctx.voice_client.play(discord.FFmpegPCMAudio(name), after=lambda e: print('done', e))
                        while not ctx.voice_client.is_done():
                              await asyncio.sleep(1)
                        await ctx.voice_client.disconnect()
                        found = True
                  else:
                        print(name)
      if found == False:
            await ctx.send("Meme sound  was not found")
      print("done playing sound")

@memesound.before_invoke
async def ensure_voice(ctx):
	if ctx.voice_client is None:
		if ctx.author.voice:
			await ctx.author.voice.channel.connect()
		else:
			await ctx.send("You are not connected to a voice channel.")
			raise commands.CommandError("Author not connected to a voice channel.")
	elif ctx.voice_client.is_playing():
		ctx.voice_client.stop()



# @bot.command()
# async def reloadmemevideo(ctx):
#       global videonames
#       await ctx.message.channel.send("Getting new meme video.")
#       size = len(videonames)
#       videonames = glob.glob("videos/*.mp4")
#       newsize = len(videonames) - size
#       await ctx.message.channel.send("Added {0} new meme video.".format(newsize))
# @bot.command()
# async def memevideo(ctx,*args):
#       print("memesound video")
#       global videonames
#       print (videonames)
#       found = False
#       if len(args) == 0:
#             await ctx.send(file = discord.File(random.choice(videonames)))
#             found = True
#       else:
#             for name in videonames:
#                   if args[0] in name:
#                         await ctx.send(file = discord.File(name))
#                         found = True
#       if found == False:
#             await ctx.send("Meme sound  was not found")
#       print("done playing sound")
@bot.command()
async def wikipedia(ctx,*args):
      print("wikipedia called")
      await wikipedia_interact(args,ctx.message.channel)

# @bot.command()
# async def tiktok(ctx,*args):
#       print("tiktok called")
#       await tiktok_interact(args,ctx.message.channel)

@bot.command()
async def lang(ctx,*args):
      print("lang called")
      #tts = gTTS('hello', lang='en')
      await ctx.message.channel.send(gtts.lang.tts_langs())       

@bot.command()
async def avatar(ctx, *, member: discord.Member=None): # set the member object to None
      member = member or ctx.author
      userAvatar = member.avatar_url
      await ctx.send(userAvatar)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    channel = discord.utils.get(bot.get_all_channels(), name='general')
    await channel.send("Hello everybody, Ready to make some memes. ")
    await channel.send("Please use - before the command EX: -say ")
      
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
            if(len(ctx.args) > 0):
                  await ctx.send("Comand {0} not found, are you retard @{1}? write correctly".format(ctx.args[0],ctx.message.author))
            else:
                  await ctx.send("Comand {0} not found, are you retard @{1}? write correctly".format(ctx.message.content,ctx.message.author))

bot.run(DISCORD_TOKEN)
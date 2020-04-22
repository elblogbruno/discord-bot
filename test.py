# -*- coding: utf-8 -*-
import discord
from chuck import ChuckNorris
from gtts import gTTS
cn = ChuckNorris()
import os
import random
from tts import loquendo_tts
from utils import audio_segment_to_voice
from utils import audio_segment_to_voice_mp3
from utils import downloadImage
from pydub import AudioSegment
from pydub.playback import play
import io
import praw

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
#    async def on_member_join(member):
#        print('Logged on as {0}!'.format(member.user))
#        channel = message.channel
#        await channel.send('Welcome new member!' + member)
    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))
        if message.author == "MemeBot#7484":
              return
        if message.content == "help":
              channel = message.channel
              await channel.send('Available commands: -chuck norris -say x -yo mama')
        if message.content == "chuck norris":
              channel = message.channel
              await channel.send('A chuck norris joke is coming for you!')
              # Get random jokes.
              data = cn.random()
              await channel.send(data)
        if message.content.split()[0] == "say":
              print(message.content.split()[0])
              print(message.content.split()[1])
              channel = message.channel
              y = message.content.replace('say','')
              await channel.send("I'll say " + y)
              tts_segment = loquendo_tts(y, "es-es")
              tts_bytes = audio_segment_to_voice_mp3(tts_segment)
              #tts = gTTS(y)
              #os.remove("message.mp3")
              #tts.save('message.mp3')
              #song = AudioSegment.from_file(io.BytesIO(tts_bytes), format="mp3")
              #song = AudioSegment.from_file(io.BytesIO(tts_bytes), format="mp3")
              file1 = discord.File('text.mp3')
              await channel.send(file=file1)
        if message.content == "yo mama":
              channel = message.channel
              await channel.send("I'll send a yo mama joke")
              with open("jokes.txt",'r',encoding = 'utf-8') as f:
                   lines = f.readlines()
                   await channel.send(random.choice(lines))
        if  message.content.split()[0] == "reddit":
              reddit = praw.Reddit(client_id='nxgE3wLXaUPIRw',
                     client_secret='d8bpGC8XER2LNeulKTvEZ6bKTjc',
                     user_agent='Comment Extraction (by /u/USERNAME)')
              channel = message.channel
              subreddit = reddit.subreddit(message.content.split()[1])
              await channel.send("Subreddit name: " + subreddit.display_name)  # Output: redditdev
              await channel.send("Subreddit title: " +subreddit.title)         # Output: reddit Development
              await channel.send("Subreddit description " +subreddit.description)   # Output: A subreddit for discussion of ...
              for submission in reddit.subreddit(message.content.split()[1]).hot(limit=int(message.content.split()[2])):
                   print(submission.title.encode('ascii', 'ignore').decode('ascii'))
                   await channel.send(submission.title.encode('ascii', 'ignore').decode('ascii'))
                   if "jpg" in submission.url:
                       name = downloadImage(submission.url)
                       await channel.send(file=discord.File("images/"+name+'.jpg'))
                       os.remove("images/"+name+'.jpg')
                   else:
                       await channel.send("There's no meme available for this subreddit post")
client = MyClient()
client.run('NzAyNTE5NzA1OTM1ODA2NTE2.XqBOgw.skXN-MA1XtH6DUrEdh39hJhKti0')

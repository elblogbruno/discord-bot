import discord
import youtube_dl
import os
import asyncio
from time import sleep
from discord import FFmpegPCMAudio
import sys


youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
	'format': 'bestaudio/best',
	'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
	'restrictfilenames': True,
	'noplaylist': True,
	'nocheckcertificate': True,
	'ignoreerrors': False,
	'logtostderr': False,
	'quiet': True,
	'no_warnings': True,
	'default_search': 'auto',
	'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
	'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
	def __init__(self, source, *, data, volume=0.5):
		super().__init__(source, volume)

		self.data = data

		self.title = data.get('title')
		self.url = data.get('url')

	@classmethod
	async def from_url(cls, url, *, loop=None, stream=False):
		loop = loop or asyncio.get_event_loop()
		data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

		if 'entries' in data:
			# take first item from a playlist
			data = data['entries'][0]

		filename = data['url'] if stream else ytdl.prepare_filename(data)
		return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


async def youtube_cutter_interact(args,ctx,bot):
	if args:
		
		channel = ctx.message.channel
		save_location_music = "sonidos/"
		save_location = save_location_music
		song_format = "mp3"
		current_format = song_format

		url = args[0]
		search_word = args[1]

		songPlace = save_location+search_word+"."+current_format

		print("Downloading song: "+ str(search_word))
		print("Song Place: " + songPlace)
		print("url: " + url)

		if os.path.exists(songPlace):
			print("Song or video already exists on the given path. Not downloading again.")
			await channel.send("Meme sound or video already exists. Not downloading again.")
		else:  
			def callback(d):
				#print(d)
				if d['status'] == 'finished':     
					print ( "has finished downloading")       
					bot.loop.create_task(channel.send("Meme sound/video downloaded entirely."))
					print("Done!") 
			ydl_opts = {
						'format': 'bestaudio',
						'postprocessors': [{
							'key': 'FFmpegExtractAudio',
							'preferredcodec': 'mp3',
							'preferredquality': '192'
						}],
						'prefer_ffmpeg': True,
						'outtmpl': '{1}{0}.%(ext)s'.format(search_word,save_location),                
						'progress_hooks': [callback] 
					}
			player = await YTDLSource.from_url(url, loop=bot.loop, stream=True)
			ctx.voice_client.play(player, after=lambda e: print("Player error: %s" % e) if e else None)
			await ctx.send("Now playing meme sound: {}".format(player.title))
			with youtube_dl.YoutubeDL(ydl_opts) as ydl:
				ydl.download([url])
	else:
		await channel.send("Incorrect, please use it like this : say 'your message' ")

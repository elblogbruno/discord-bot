import discord
import youtube_dl
from discord.ext import commands
from discord import FFmpegPCMAudio
import sys

client = commands.Bot(command_prefix = "!")

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

@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))

@client.command(pass_context=True)
async def join(ctx):
	print("join")
	channel = ctx.message.author.voice.channel
	await channel.connect()

@client.command(pass_context=True)
async def leave(ctx):
	print("leave")
	channel = ctx.message.author.voice.channel
	await ctx.voice_client.disconnect()

@client.command(pass_context=True)
async def yt(ctx, url):
	async with ctx.typing():
		player = await YTDLSource.from_url(url, loop=client.loop, stream=True)
		ctx.voice_client.play(player, after=lambda e: print("Player error: %s" % e) if e else None)

	await ctx.send("Now playing: {}".format(player.title))

@client.command(pass_context=True)
async def volume(ctx, volume: int):
	if ctx.voice_client is None:
		return await ctx.send("Kein Audiochannel gefunden")
	ctx.voice_client.source.volume = volume / 100
	await ctx.send("Changed volume to {}".format(volume))


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

@client.command(pass_context=True)
async def shutdown(ctx):
	sys.exit()


client.run("NzAyNTE5NzA1OTM1ODA2NTE2.XqCHNg.R9NnzTYk4qlvP2uRAS-_y-oCJSA")
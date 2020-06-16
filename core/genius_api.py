import lyricsgenius
import discord
import textwrap
from core.loquendo_api_tss import loquendo_interact
from secrets import GENIUS_TOKEN
genius = lyricsgenius.Genius(GENIUS_TOKEN)
#genius.verbose = False

def check(m):
    return m.content == 'yes' and m.channel == channel and m.author == author
async def genius_interact(args,channel,author,bot):
    if len(args) > 0:
        name = args[0]
        song = ""
        shortened_wrapped = ""
        try:
            if len(args) > 1:
                artist_name = args[1]
                await channel.send("Searching song {0} by {1}".format(name,artist_name))
                song = genius.search_song(name,artist_name)
            else:
                await channel.send("Searching song {0}".format(name))
                song = genius.search_song(name)
        except:
            await channel.send("Song not found")
        
        try:
            print("Song lenght {0}".format(len(song.lyrics)))
        except:
            await channel.send("Song not found")
        
        if len(song.lyrics) > 2000:
            wrapper = textwrap.TextWrapper(width=100)
            lyrics = song.lyrics
            shortened = textwrap.shorten(text=str(lyrics), width=2000) 
            shortened_wrapped = wrapper.fill(text=shortened) 
            await channel.send(str(shortened_wrapped))
        else:
            shortened_wrapped = song.lyrics
            await channel.send(str(shortened_wrapped))
        await channel.send("Here's the song web {0}".format(song.url))
        await channel.send('{0} say yes if you want me to sing it!'.format(author))

        msg = (await bot.wait_for("message"))
        
        if msg.content == "yes" and msg.author == author:
            await channel.send("Hello @{0}! I'll sing for you {1}".format(author,name))
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="a song"))
            await loquendo_interact(shortened_wrapped,channel,True)
        else:
            await channel.send("Ok I'll shut the fuck up".format(author,name))
    else:
        await channel.send("Please tell me the song name: genius 'name' 'author(optional)'")
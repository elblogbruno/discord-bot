import lyricsgenius
import discord
import textwrap
from loquendo_api_tss import loquendo_interact
from secrets import GENIUS_TOKEN
genius = lyricsgenius.Genius(GENIUS_TOKEN)
#genius.verbose = False
async def genius_interact(args,channel,author,client):
     if len(args) > 1:
        name = args[0]
        song = ""
        if len(args) > 2:
            artist_name = args[1]
            await channel.send("Searching song {0} by {1}".format(name,artist_name))
            song = genius.search_song(name,artist_name)
        else:
            await channel.send("Searching song {0}".format(name))
            song = genius.search_song(name)
            
        print("Song lenght {0}".format(len(song.lyrics)))
        wrapper = textwrap.TextWrapper(width=100)
        lyrics = song.lyrics
        shortened = textwrap.shorten(text=str(lyrics), width=2000) 
        shortened_wrapped = wrapper.fill(text=shortened) 
        await channel.send(shortened_wrapped)
        await channel.send("Here's the song web {0}".format(song.url))
        await channel.send('{0} say yes if you want me to sing it!'.format(author))

        def check(m):
            return m.content == 'yes' and m.channel == channel and m.author == author
        msg = await client.wait_for('message', check=check)
        if msg:
            await channel.send("Hello @{0}! I'll sing for you {1}".format(author,name))
            await loquendo_interact(shortened_wrapped,channel,True)
        else:
            await channel.send("Ok  I'll shut the fuck up".format(author,name))
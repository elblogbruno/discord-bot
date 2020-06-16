from core.config import GTTS_LANGUAGE
from core.tts import loquendo_tts
from core.utils import audio_segment_to_voice_mp3
import asyncio
from discord.voice_client import VoiceClient
from gtts import gTTS
import discord
#from utils import audio_segment_to_voice
async def loquendo_interact(message,bot,ctx,channel,song):
    
    if song:
       print ( "LOQUENDO A SONG")
       tts_segment = loquendo_tts(str(message), GTTS_LANGUAGE)
       tts_bytes = audio_segment_to_voice_mp3(tts_segment)
       await channel.send(file=tts_bytes)
    else:
        #lang = " "
        finalMessage = " "
        if message:
            if len(message) > 4:
                finalMessage = ' '.join(message)
            else:
                finalMessage = message[0]
            print(str(finalMessage.encode('utf-8')))
            await channel.send("I'll say " + str(finalMessage))
            lang = GTTS_LANGUAGE
            if len(message) > 1:
                lang = message[1]
                finalMessage.replace(lang,'')
            tts_segment = loquendo_tts(str(finalMessage), lang)
            tts_bytes = audio_segment_to_voice_mp3(tts_segment)
            #file1 = discord.File('text.mp3')
            await channel.send(file=tts_bytes)
            # only play music if user is in a voice channel
            user = ctx.message.author
            if user != None:
                channel = user.voice.channel
                if not ctx.voice_client.is_playing():
                    ctx.voice_client.play(discord.FFmpegPCMAudio('text.mp3'), after=lambda e: print('done', e))
                while not ctx.voice_client.is_done():
                    await asyncio.sleep(1)
                await ctx.voice_client.disconnect()
            else:
                await channel.say('User is not in a channel.')
        else:
            await channel.send("Incorrect, please use it like this : say 'your message' ")

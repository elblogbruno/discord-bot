from config import GTTS_LANGUAGE
from tts import loquendo_tts
from utils import audio_segment_to_voice_mp3
from gtts import gTTS
import discord
#from utils import audio_segment_to_voice
async def loquendo_interact(message,channel,song):
    
    if song:
       tts_segment = loquendo_tts(message, GTTS_LANGUAGE)
       tts_bytes = audio_segment_to_voice_mp3(tts_segment)
       await channel.send(file=tts_bytes)
    else:
        print(message.split("'"))
        a_list = message.split("'")
        without_empty_strings = []
        without_empty_strings = [x for x in a_list if x]
        if len(a_list) > 2:
            
            if len(without_empty_strings) > 3:
                without_empty_strings =  [string for string in without_empty_strings if string != "" and string != " "]
                print(without_empty_strings)
            print (without_empty_strings)
            #y = message.content.replace('say',''
            
            y = without_empty_strings[1]
            await channel.send("I'll say " + y)
            tts_segment = loquendo_tts(y, GTTS_LANGUAGE)
            tts_bytes = audio_segment_to_voice_mp3(tts_segment)
            #file1 = discord.File('text.mp3')
            await channel.send(file=tts_bytes)
        else:
            await channel.send("Incorrect, please use it like this : say 'your message' ")

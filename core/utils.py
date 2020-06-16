import discord
from io import BytesIO
from pydub import AudioSegment
import math
import requests
import random
import string
import unicodedata
import os
def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])
def downloadImage(pic_url):
    name = randomString()
    print(pic_url)
    with open('images/'+name+'.jpg', 'wb') as handle:
        response = requests.get(pic_url, stream=True)

        if not response.ok:
            print(response)

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)
    return name
def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))
def overlay_sound_perfect_loop(base: AudioSegment, overlay: AudioSegment) -> AudioSegment:
    duration_base = len(base)
    duration_overlay = len(overlay)
    times_looped = math.ceil(duration_base / duration_overlay)
    silence_time_needed = duration_overlay * times_looped - duration_base

    if silence_time_needed > 0:
        base = base.append(
            AudioSegment.silent(duration=max(silence_time_needed, 100)),
            crossfade = 100
        )
    
    return base.overlay(overlay, times = times_looped)

def audio_segment_to_voice(segment: AudioSegment) -> BytesIO:
    b = BytesIO()
    segment.export(b, format = "ogg", codec = "libopus")
    return b
def audio_segment_to_voice_mp3(segment: AudioSegment) -> discord.File:
    b = BytesIO()
    segment.export('text.mp3', format = "mp3", codec = "mp3")
    file =  discord.File('text.mp3')
    return file
def cut_song(songPlace,name,timeStart,timeEnd):
    print(songPlace + " " + name + timeStart + timeEnd)

    startMin = int(timeStart.split(":")[0])
    startSec = int(timeStart.split(":")[1])

    endMin = int(timeEnd.split(":")[0])
    endSec = int(timeEnd.split(":")[1])
    # Time to miliseconds
    startTime = startMin*60*1000+startSec*1000
    endTime = endMin*60*1000+endSec*1000
    print(str(startTime) + " "+ str(endTime))
    #finalPlace = songPlace + ".mp3"
    if os.path.isfile(songPlace):
        song = AudioSegment.from_mp3(songPlace)
        extract = song[startTime:endTime]
        # Saving
        extract.export("sonidos/"+name + "-cut.mp3", format="mp3")
    elif os.path.isfile(songPlace):
        #finalPlace = songPlace+".m4a"
        song = AudioSegment.from_file(songPlace,format='m4a')
        extract = song[startTime:endTime]
        # Saving
        extract.export("sonidos/"+name + "-cut.mp3", format="mp3")
    os.remove(songPlace)
    return True

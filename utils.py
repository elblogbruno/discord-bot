from io import BytesIO
from pydub import AudioSegment
import math
import requests
import random
import string
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
def audio_segment_to_voice_mp3(segment: AudioSegment) -> BytesIO:
    b = BytesIO()
    segment.export('text.mp3', format = "mp3", codec = "mp3")
    return b

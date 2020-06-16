import wikipedia
import discord
import random
#from utils import audio_segment_to_voice
async def wikipedia_interact(message,channel):
    finalMessage = " "
    summary = " "
    if message:
        if len(message) > 1:
            finalMessage = ' '.join(message)
        else:
            finalMessage = message[0]
        wikipedia.set_lang("es")
        print(str(finalMessage.encode('utf-8')))
        await channel.send("Searching {0} on Wikipedia".format(str(finalMessage)))
        try:
            summary = wikipedia.summary(str(finalMessage))
            await channel.send(str(summary))
        except wikipedia.exceptions.DisambiguationError as e:
            #print(str(e.options.encode('utf-8')))
            await channel.send("{0} Might mean one of those things. Choose one: wikipedia '{1}' for example".format(str(summary),str(e.options[random.randint(0,len(e.options))])))
            for option in e.options:
                await channel.send(str(option))
        except wikipedia.exceptions.PageError as e:
                await channel.send("{0} does not exist on wikipedia!".format(e))
        
    else:
        await channel.send("Incorrect, please use it like this : say 'your message' ")

import requests
import random
import os
import discord
from core.utils import downloadImage
import re
import string
from secrets import MEME_USERNAME
from secrets import MEME_PASSWORD
async def meme_interact(args,channel):
    # api-endpoint 
    CAPTION_URL = "https://api.imgflip.com/caption_image"

    if len(args) > 0:
        template_id = "112126428"
        if len(args) == 2:
            await channel.send("Getting random meme template")
            template_id = getRandomMemeId() #"112126428"
        elif args[2].isdecimal() == False:
            await channel.send("Getting " + args[2] + " meme template")
            template_id = getMemeId(args[2]) #"112126428"
        elif args[2].isdecimal():
            template_id =  args[2]
        username = MEME_USERNAME
        password = MEME_PASSWORD
        text0 = args[0]
        text1 = args[1]
        # defining a params dict for the parameters to be sent to the API 
        PARAMS = {'template_id':template_id,'username':username,'password':password,'text0':text0,'text1':text1}
        
        # sending get request and saving the response as response object 
        r = requests.post(url = CAPTION_URL, params = PARAMS) 
        
        # extracting data in json format 
        data = r.json() 
        
        print(data)
        # extracting latitude, longitude and formatted address  
        # of the first matching location 
        success = data['success']
        if success:
            meme_url = data['data']['url']
            page_url = data['data']['page_url']
            #name = downloadImage(meme_url)
            await channel.send("This is the meme url: " + page_url)
            #await channel.send(file=discord.File("memeimages/"+name+'.jpg'))
            #os.remove("memeimages/"+name+'.jpg')
    else:
        await channel.send("Please tell me the meme text TOP and text DOWN: meme 'text that will be top' 'text on down' 'meme template name(optional)'")

def getRandomMemeId():
    URL = "https://api.imgflip.com/get_memes"
    r = requests.get(url = URL) 
    
    # extracting data in json format 
    data = r.json() 
    memes = data['data']['memes']
    randomIndex = random.randint(0, 100)
    randomMemeID =  memes[randomIndex]['id']
    print(randomMemeID)
    return randomMemeID
def getMemeId(name):
    URL = "https://api.imgflip.com/get_memes"
    r = requests.get(url = URL) 
    # extracting data in json format 
    data = r.json() 
    memeFoundNameID = 0
    memes = data['data']['memes']
    for meme in memes:
        if name.lower() in meme['name'].lower():
            memeFoundNameID = meme['id']
            break
    print(memeFoundNameID)
    return memeFoundNameID
async def getAllMemes():
    URL = "https://api.imgflip.com/get_memes"
    r = requests.get(url = URL) 
    # extracting data in json format 
    data = r.json() 
    memes = data['data']['memes']
    for meme in memes:
        await channel.send(meme['name'] + ": "+ meme['url'])

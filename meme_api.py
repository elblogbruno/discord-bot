import requests
import random
import os
import discord
from utils import downloadImage
import re 
import string 
from parse import compile
from secrets import MEME_USERNAME
from secrets import MEME_PASSWORD
async def meme_interact(message,channel):
    # api-endpoint 
    CAPTION_URL = "https://api.imgflip.com/caption_image"

    print(message.split("'"))
    a_list = message.split("'")
    without_empty_strings = []
    #for string in a_list:
    #    if (string != " " and string != ""):
    #        without_empty_strings.append(string)
    ##print (without_empty_strings)
    without_empty_strings = ' '.join(a_list).split()
    print (without_empty_strings)
    template_id = "112126428"
    print(len(without_empty_strings))
    if len(without_empty_strings) == 3:
        await channel.send("Getting random meme template")
        template_id = getRandomMemeId() #"112126428"
    elif without_empty_strings[3].isdecimal() == False:
        await channel.send("Getting " + without_empty_strings[3] + " meme template")
        template_id = getMemeId(without_empty_strings[3]) #"112126428"
    elif without_empty_strings[3].isdecimal():
        template_id =  without_empty_strings[3]
    username = MEME_USERNAME
    password = MEME_PASSWORD
    text0 = without_empty_strings[1]
    text1 = without_empty_strings[2]
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

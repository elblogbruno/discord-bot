import discord
import time
import giphy_client
from giphy_client.rest import ApiException
from pprint import pprint
from secrets import GIPHY_TOKEN
#import filter
# create an instance of the API class
api_instance = giphy_client.DefaultApi()
api_key = GIPHY_TOKEN # str | Giphy API Key.
#q = 'cheeseburgers' # str | Search query term or prhase.
limit = 1 # int | The maximum number of records to return. (optional) (default to 25)
offset = 0 # int | An optional results offset. Defaults to 0. (optional) (default to 0)
rating = 'g' # str | Filters results by specified rating. (optional)
lang = 'en' # str | Specify default country for regional content; use a 2-letter ISO 639-1 country code. See list of supported languages <a href = \"../language-support\">here</a>. (optional)
fmt = 'json' # str | Used to indicate the expected response format. Default is Json. (optional) (default to json)

async def giphy_interact(message,channel):
    print(message.split("'"))
    a_list = message.split("'")
    without_empty_strings = [x for x in a_list if x]
    if len(a_list) > 2:

        #for string in a_list:
        #    if (string != " " and string != ""):
        #        without_empty_strings.append(string)
        without_empty_strings =  [string for string in without_empty_strings if string != "" and string != " "]
        # if len(a_list) > 3:
        #     without_empty_strings =  [string for string in without_empty_strings if string != "" and string != " "]
        print (without_empty_strings)
        print (len(without_empty_strings))
        if len(without_empty_strings) == 3:
            limit = int(without_empty_strings[2])
            lang = 'en'
        elif len(without_empty_strings) == 4:
            limit = int(without_empty_strings[2])
            lang = without_empty_strings[3]
        else:
            limit = 1
            lang = 'en'
        try:
            # Search Endpoint
            q = without_empty_strings[1]
            await channel.send("Searching for gif {0} in {1} language".format(q,lang))
            await channel.send("Gonna send you {0} gif(s)".format(limit))
            api_response = api_instance.gifs_search_get(api_key, q, limit=limit, offset=offset, rating=rating, lang=lang, fmt=fmt)
            #pprint(api_response)
            for gif in api_response.data:
                url =  gif.embed_url
                await channel.send(url)
        except ApiException as e:
            print("Exception when calling DefaultApi->gifs_search_get: %s\n" % e)
    else:
         print("There's no gif name")
         await channel.send("Please insert a name of the gif: gif 'name'")

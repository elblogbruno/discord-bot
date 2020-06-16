from TikTokApi import TikTokApi
import discord
api = TikTokApi(True)


async def tiktok_interact(message,channel):
    results = 10
    trending = api.trending(results)

    for tiktok in trending:
        # Prints the text of the tiktok
        print(tiktok['desc'])
        await channel.send(tiktok['video']['cover'])

    print(len(trending))

from TikTokApi import TikTokApi
api = TikTokApi(True)

results = 10

trending = api.trending(results)

for tiktok in trending:
    # Prints the text of the tiktok
    print(tiktok['desc'])

print(len(trending))

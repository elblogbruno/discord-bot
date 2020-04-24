import os
import praw
import discord
from utils import downloadImage
from secrets import REDDIT_ID
from secrets import REDDIT_SECRET
reddit = praw.Reddit(client_id=REDDIT_ID,
                     client_secret=REDDIT_SECRET,
                     user_agent='Comment Extraction (by /u/USERNAME)')
async def reddit_interact(query,channel):

    post_list = [ ]
    subreddit = reddit.subreddit(query.split()[1])
    await channel.send("Subreddit name: " + subreddit.display_name)  # Output: redditdev
    await channel.send("Subreddit title: " +subreddit.title)         # Output: reddit Development
    await channel.send("Subreddit description " +subreddit.description)   # Output: A subreddit for discussion of ...
    await channel.send("Gonna send you " + query.split()[2] + " memes from "+subreddit.description)
    category = "hot"
    if len(query.split()) < 3:
        category = "hot"
        post_list = reddit.subreddit(query.split()[1]).hot(limit=int(query.split()[2]))
    else:
        if query.split()[3] == "top":
            post_list = reddit.subreddit(query.split()[1]).top(limit=int(query.split()[2]))
        if query.split()[3] == "rising":
            category = "rising"
            post_list = reddit.subreddit(query.split()[1]).rising(limit=int(query.split()[2]))
        if query.split()[3] == "best":
            category = "best"
            post_list = reddit.subreddit(query.split()[1]).best(limit=int(query.split()[2]))
        if query.split()[3] == "new":
            category = "new"
            post_list = reddit.subreddit(query.split()[1]).new(limit=int(query.split()[2]))
        if query.split()[3] == "hot":
            category = "hot"
            post_list = reddit.subreddit(query.split()[1]).hot(limit=int(query.split()[2]))
    
    await channel.send("Choosing " + category + " memes")
    for submission in post_list:
        print(submission.title.encode('ascii', 'ignore').decode('ascii'))
        if "jpg" in submission.url:
                await channel.send(submission.title.encode('ascii', 'ignore').decode('ascii'))
                await channel.send("------------------")
                name = downloadImage(submission.url)
                await channel.send(file=discord.File("images/"+name+'.jpg'))
                os.remove("images/"+name+'.jpg')
        else:
                await channel.send(submission.title.encode('ascii', 'ignore').decode('ascii') + "- There's no meme available for this subreddit post")
                await channel.send("------------------")
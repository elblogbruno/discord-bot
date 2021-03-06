import os
import praw
import discord
from core.utils import downloadImage
from secrets import REDDIT_ID
from secrets import REDDIT_SECRET
reddit = praw.Reddit(client_id=REDDIT_ID,
                     client_secret=REDDIT_SECRET,
                     user_agent='Comment Extraction (by /u/USERNAME)')
async def reddit_interact(channel,args):
    if len(args) > 0:
        post_list = [ ]
        subreddit = reddit.subreddit(args[0])
        await channel.send("Subreddit name: " + subreddit.display_name)  # Output: redditdev
        await channel.send("Subreddit title: " +subreddit.title)         # Output: reddit Development
        await channel.send("Subreddit description " +subreddit.description)   # Output: A subreddit for discussion of ...
        await channel.send("Gonna send you " + args[1] + " memes from "+subreddit.display_name)
        category = "hot"
        if len(args) < 3:
            category = "hot"
            post_list = reddit.subreddit(args[0]).hot(limit=int(args[1]))
        else:
            if args[2] == "top":
                post_list = reddit.subreddit(args[0]).top(limit=int(args[1]))
            if args[2] == "rising":
                category = "rising"
                post_list = reddit.subreddit(args[0]).rising(limit=int(args[1]))
            if args[2] == "best":
                category = "best"
                post_list = reddit.subreddit(args[0]).best(limit=int(args[1]))
            if args[2] == "new":
                category = "new"
                post_list = reddit.subreddit(args[0]).new(limit=int(args[1]))
            if args[2] == "hot":
                category = "hot"
                post_list = reddit.subreddit(args[0]).hot(limit=int(args[1]))
        
        await channel.send("Choosing " + category + " memes")
        for submission in post_list:
            print(str(submission.title.encode('utf-8')))
            await channel.send(str(submission.title))
            await channel.send("------------------")
            await channel.send(submission.url)
            # if "jpg" in submission.url:
            #         await channel.send(str(submission.title))
            #         await channel.send("------------------")
            #         #name = downloadImage(submission.url)
            #         #await channel.send(file=discord.File("images/"+name+'.jpg'))
            #         await channel.send(submission.url)
            #         #os.remove("images/"+name+'.jpg')
            # else:
            #         await channel.send(str(submission.title) + "- There's no meme available for this subreddit post")
            #         await channel.send("------------------")
    else:
        await channel.send("Please tell me the subreddit name: reddit 'name' 'limit (optional)' 'type(optional)'")
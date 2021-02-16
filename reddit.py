import praw
import pandas as pd
import datetime as dt

from praw.models import MoreComments


def readit():
    reddit = praw.Reddit(client_id='mpS_DJ7JYUgH4w',
                         client_secret='LsL8Sr14gmI2cEB6jde6dpxpaMRDdg',
                         user_agent='amsia1',
                         username='sbhattathiri',
                         password='UmaMaheshwaran07$')

    rcricket = reddit.subreddit('Cricket')


    hot_cricket = rcricket.hot(limit=10)

    num = 0
    for post in hot_cricket:
        if 'Match Thread:' in post.title:
            submission = reddit.submission(id=post.id)
            for top_level_comment in submission.comments:
                if isinstance(top_level_comment, MoreComments):
                    continue
                print(f'{top_level_comment.body} : {top_level_comment.score}')
                num += 1
                if num > 10:
                    break


if __name__ == '__main__':
    readit()
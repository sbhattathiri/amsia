import praw
import pandas as pd
import datetime as dt
import argparse

from praw.models import MoreComments


def read_it():
    reddit = praw.Reddit(client_id='',
                         client_secret='',
                         user_agent='',
                         username='',
                         password='')

    rcricket = reddit.subreddit('Cricket')

    hot_cricket = rcricket.hot(limit=100)

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
    read_it()

import argparse

import praw
from praw.models import MoreComments


class ReadIt():
    def __init__(self, client_id, client_secret, user_agent, user_name, password, subreddits):
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent
        self.user_name = user_name
        self.password = password
        self.subreddits = subreddits

    def print(self):
        print(self.client_id)
        print(self.client_secret)
        print(self.user_agent)
        print(self.user_name)
        print(self.password)
        print(self.subreddits)

    def scrape(self):
        reddit = praw.Reddit(client_id=self.client_id,
                             client_secret=self.client_secret,
                             user_agent=self.user_agent,
                             username=self.user_name,
                             password=self.password)

        rcricket = reddit.subreddit('Cricket')

        hot_cricket = rcricket.hot(limit=10)

        num = 0
        for post in hot_cricket:
            print(post.title)
            if 'Match Thread:' in post.title:
                submission = reddit.submission(id=post.id)
                for top_level_comment in submission.comments:
                    if isinstance(top_level_comment, MoreComments):
                        continue
                    print(f'{top_level_comment.body} : {top_level_comment.score}')
                    num += 1
                    if num > 10:
                        break


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--client_id", help="client id")
    parser.add_argument("--client_secret", help="client secret")
    parser.add_argument("--user_agent", help="user agent")
    parser.add_argument("--username", help="username")
    parser.add_argument("--password", help="password")
    parser.add_argument("--subreddits", nargs='+', help="list of subs")
    args = parser.parse_args()

    read_it = ReadIt(client_id=args.client_id,
                     client_secret=args.client_secret,
                     user_agent=args.user_agent,
                     user_name=args.username,
                     password=args.password,
                     subreddits=args.subreddits)

    read_it.scrape()


if __name__ == '__main__':
    main()

import argparse

import praw
import pymongo
from praw.models import MoreComments


class ReadIt:
    def __init__(self,
                 client_id,
                 client_secret,
                 user_agent,
                 user_name,
                 password,
                 subreddits,
                 mongo_db_host,
                 mongo_db_port,
                 mongo_db_database_name,
                 mongo_db_collection_name,
                 mongo_db_username,
                 mongo_db_password
                 ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent
        self.user_name = user_name
        self.password = password
        self.subreddits = subreddits
        self.mongo_db_host = mongo_db_host
        self.mongo_db_port = mongo_db_port
        self.mongo_db_database_name = mongo_db_database_name
        self.mongo_db_collection_name = mongo_db_collection_name
        self.mongo_db_username = mongo_db_username
        self.mongo_db_password = mongo_db_password

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

        data = []
        for sub in self.subreddits:
            rsub = reddit.subreddit(sub)

            new_posts = rsub.new(limit=10)

            max_posts = 10
            post_num = 0

            max_comments = 10

            for post in new_posts:
                datum = {}
                comment_num = 0
                submission = reddit.submission(id=post.id)
                for top_level_comment in submission.comments:

                    if isinstance(top_level_comment, MoreComments):
                        continue


                    datum['post_title'] = post.title
                    datum['post_score'] = post.score
                    if post.author is not None:
                        datum['post_author'] = post.author.name
                        datum['post_author_verified_email'] = post.author.has_verified_email
                        datum['post_author_karma'] = post.author.comment_karma
                    datum['post_created'] = post.created_utc
                    datum['comment_text'] = top_level_comment.body
                    datum['comment_score'] = top_level_comment.score
                    if top_level_comment.author is not None:
                        datum['comment_author'] = top_level_comment.author.name
                        datum['comment_author_verified_email'] = top_level_comment.author.has_verified_email
                        datum['comment_author_karma'] = top_level_comment.author.comment_karma
                        datum['comment_issubmitter'] = top_level_comment.is_submitter
                    datum['comment_created'] = top_level_comment.created_utc
                    datum['comment_subreddit'] = sub

                    data.append(datum.copy())

                    comment_num += 1
                    if comment_num > max_comments:
                        break

                post_num += 1
                if post_num > max_posts:
                    break

        return data

    def insert_into_mongo(self, data):
        mongo_client = pymongo.MongoClient(f'mongodb://{self.mongo_db_host}:{self.mongo_db_port}/')
        mongo_database = mongo_client[self.mongo_db_database_name]
        mongo_collection = mongo_database[self.mongo_db_collection_name]

        num_doc_inserted = mongo_collection.insert_many(data)
        return num_doc_inserted


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--client_id", help="client id")
    parser.add_argument("--client_secret", help="client secret")
    parser.add_argument("--user_agent", help="user agent")
    parser.add_argument("--username", help="username")
    parser.add_argument("--password", help="password")
    parser.add_argument("--subreddits", nargs='+', help="list of subs")
    parser.add_argument("--mongo_db_host", help="mongo db host")
    parser.add_argument("--mongo_db_port", help="mongo db port")
    parser.add_argument("--mongo_db_database_name", help="mongo db database name")
    parser.add_argument("--mongo_db_collection_name", help="mongo db collection name")
    parser.add_argument("--mongo_db_username", help="mongo db username")
    parser.add_argument("--mongo_db_password", help="mongo db password")
    args = parser.parse_args()

    read_it = ReadIt(client_id=args.client_id,
                     client_secret=args.client_secret,
                     user_agent=args.user_agent,
                     user_name=args.username,
                     password=args.password,
                     subreddits=args.subreddits,
                     mongo_db_host=args.mongo_db_host,
                     mongo_db_port=args.mongo_db_port,
                     mongo_db_database_name=args.mongo_db_database_name,
                     mongo_db_collection_name=args.mongo_db_collection_name,
                     mongo_db_username=args.mongo_db_username,
                     mongo_db_password=args.mongo_db_password
                     )

    data = read_it.scrape()
    num_doc_inserted = read_it.insert_into_mongo(data=data)
    print(num_doc_inserted)


if __name__ == '__main__':
    main()

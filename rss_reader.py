import argparse
from bs4 import BeautifulSoup
import feedparser
import json


class Content:

    def __init__(self):
        """Creating empty entry objects."""
        self.title = ''
        self.date = ''
        self.link = ''
        self.content = ''

    def output(self):
        print('\n' + 'Title: ' + self.title)
        print('Publication Date: ' + self.date)
        print('Link: ' + self.link + '\n')
        print(self.content)


def getting_arguments():
    parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader.', add_help=True)
    parser.add_argument('source', type=str, help='RSS URL')
    parser.add_argument('--version', action='store_true', help='Print version info')
    parser.add_argument('--json', action='store_true', help='Print result as JSON in stdout')
    parser.add_argument('--verbose', action='store_true', help='Outputs verbose status messages')
    parser.add_argument('--limit', type=int, help='Limit news topics if this parameter provided')
    args = parser.parse_args()
    return args


def getting_feed(args):
    thefeed = feedparser.parse(args.source)
    return thefeed


def creating_list_of_entries(thefeed):
    """Creating list of entry objects with readable news"""
    entries = thefeed.entries
    news_list = []
    for entry in entries:
        news = Content()
        news.feed = thefeed.feed.get("title", "")
        news.title = str(BeautifulSoup(entry.title, "html.parser"))
        try:
            news.date = str(BeautifulSoup(entry.published, "html.parser"))
        except AttributeError:
            news.date = 'Date: this article has no date.'
        try:
            news.link = str(entry.link)
        except AttributeError:
            news.link = 'Link: this article has no link.'
        content = BeautifulSoup(entry.summary, "html.parser")
        news.content = content.text
        news_list.append(news)
    return news_list


def output(args, thefeed, news_list):
    """Outputing news"""
    print('Feed: ', thefeed.feed.get("title", ""))
    if args.limit != 0:
        limit = args.limit
        for news in news_list[:limit]:
            news.output()
    elif args.limit == 0:
        print('Limit = 0, no news to print.')
    else:
        for news in news_list:
            news.output()


def convert_to_json(news_list, args, thefeed):
    news_list_json = []
    feed = thefeed.feed.get("title", "")
    for news in news_list:
        news_dict = {
            feed: {
                'Title': news.title,
                'Publication Date': news.date,
                'Link': news.link,
                'Content': [
                    news.content
                ]
            }
        }
        news_list_json.append(news_dict)
    if args.limit != 0:
        limit = args.limit
        for news in news_list_json[:limit]:
            print(json.dumps(news, indent=4, ensure_ascii=False))
    elif args.limit == 0:
        print('Limit = 0, no news to print.')
    else:
        for news in news_list_json:
            print(news)

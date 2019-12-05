import argparse
from bs4 import BeautifulSoup
import feedparser
import json
import logging
import sys


class Content:
    """Determining functions to create empty entry(news object) and output it."""

    def __init__(self):
        """Creating empty entry object."""
        self.title = ''
        self.date = ''
        self.link = ''
        self.content = ''

    def output(self):
        """Print entry to stdout."""
        print('\n' + 'Title: ' + self.title)
        print('Publication Date: ' + self.date)
        print('Link: ' + self.link + '\n')
        print(self.content)


def logger(args):
    """Creating script_logger with 2 handlers.

    verbose_handler has level 'DEBUG' and prints all logs in stdout if --verbose argument is provided.
    standard_handler has level 'DEBUG' and prints only important logs.
    """
    script_logger = logging.getLogger('rss_logger')
    script_logger.setLevel(logging.DEBUG)
    standard_handler = logging.StreamHandler()
    standard_handler.setLevel(logging.WARNING)
    standard_formatter = logging.Formatter('%(asctime)s - %(message)s')
    standard_handler.setFormatter(standard_formatter)
    verbose_handler = logging.StreamHandler()
    verbose_handler.setLevel(logging.DEBUG)
    verbose_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    verbose_handler.setFormatter(verbose_formatter)
    if args.verbose:
        script_logger.addHandler(verbose_handler)
    else:
        script_logger.addHandler(standard_handler)
    return script_logger


def getting_arguments():
    """Parsing arguments from command line."""
    parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader.', add_help=True)
    parser.add_argument('source', type=str, help='RSS URL')
    parser.add_argument('--version', action='store_true', help='Print version info')
    parser.add_argument('--json', action='store_true', help='Print result as JSON in stdout')
    parser.add_argument('--verbose', action='store_true', help='Outputs verbose status messages')
    parser.add_argument('--limit', type=int, help='Limit news topics if this parameter provided')
    args = parser.parse_args()
    return args


def getting_feed(args, script_logger):
    """Simply getting unreadable feed from URL specified in 'source'."""
    script_logger.info('Getting feed.')
    thefeed = feedparser.parse(args.source)
    script_logger.info('Feed was get successfully.')
    return thefeed


def creating_news_list(thefeed, script_logger):
    """Creating list of entry objects with readable news."""
    script_logger.info('Creating list of news entries.')
    entries = thefeed.entries
    news_list = []
    for entry in entries:
        news = Content()
        news.feed = thefeed.feed.get('title', '')
        news.title = str(BeautifulSoup(entry.title, 'html.parser'))
        try:
            news.date = str(BeautifulSoup(entry.published, 'html.parser'))
        except AttributeError:
            script_logger.warning('Current article has no date.')
            news.date = 'Date: this article has no date.'
        try:
            news.link = str(entry.link)
        except AttributeError:
            script_logger.warning('Current article has no link.')
            news.link = 'Link: this article has no link.'
        try:
            content = BeautifulSoup(entry.summary, 'html.parser')
            news.content = content.text
        except AttributeError:
            script_logger.warning('Current article has no content.')
            news.content = 'Content: this article has no content.'
        news_list.append(news)
    script_logger.info('List of news was created successfully.')
    return news_list


def limit_news_list(news_list, args, script_logger):
    script_logger.info('Creating limit list of news entries.')
    limit = args.limit
    news_list = news_list[:limit]
    script_logger.info('Limit list of news was created successfully.')
    return news_list


def output(news_list, thefeed, script_logger):
    """Output news."""
    script_logger.info('Please, read news.')
    print('Feed: ', thefeed.feed.get('title', ''))
    for news in news_list:
        news.output()


def output_in_json(news_list, thefeed, script_logger):
    """Output news in json format."""
    news_list_json = []
    feed = thefeed.feed.get('title', '')
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
    script_logger.info('Please, read news in json format.')
    for news in news_list_json:
        print(json.dumps(news, indent=4, ensure_ascii=False))


def print_version(script_logger):
    """Simply prints version of rss_reader.py script."""
    script_logger.info('Check program version.')
    print('rss_reader, version 1.0')
    sys.exit()

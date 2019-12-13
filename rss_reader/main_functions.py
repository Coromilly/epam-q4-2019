"""This module contains class and functions for rss_reader work.

Class:
class Content(object) has constructor for entry(news object) objects and method outputing() to print them to stdout

Functions:
logger(args) returns script_logger
getting_arguments() returns args
getting_feed(args, script_logger) returns thefeed
creating_news_list(thefeed, script_logger) returns news_list
limit_news_list(news_list, args, script_logger) returns news_list
output(news_list, thefeed, script_logger) returns None
output_in_json(news_list, thefeed, script_logger) returns None
print_version(script_logger) returns version
"""
import argparse
from bs4 import BeautifulSoup
from check_functions import Error, limit_arg_check
from datetime import datetime
import feedparser
import json
import logging


class Content(object):
    """Determining functions to create empty entry(news object) and output it."""

    def __init__(self):
        """Creating empty entry object."""
        self.title = ''
        self.date = ''
        self.link = ''
        self.content = ''
        self.source = ''
        self.rss_link = ''
        self.images = ''

    def outputing(self):
        """Print entry to stdout."""
        print('\n' + 'Title: ' + self.title)
        print('Publication Date: ' + self.date)
        print('Link: ' + self.link + '\n')
        print(self.content + '\n')
        print('Source: ', self.source)
        print('Images: ', self.images)
        print('-' * 120)


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
    parser.add_argument('--date', type=convert_date,
                        help='Takes a date in %Y%m%d format. '
                             'The cashed news from the specified day will be printed out')
    args = parser.parse_args()
    return args


def getting_feed(args, script_logger):
    """Simply getting unreadable feed from URL specified in 'source'."""
    script_logger.info('Getting feed.....')
    thefeed = feedparser.parse(args.source)
    script_logger.info('Feed was get successfully.')
    return thefeed


def creating_news_list(thefeed, script_logger):
    """Creating list of entry objects with readable news."""
    script_logger.info('Creating list of news entries.....')
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
            news.date = 'This article has no date.'
        try:
            news.link = str(entry.link)
        except AttributeError:
            script_logger.warning('Current article has no link.')
            news.link = 'This article has no link.'
        try:
            content = BeautifulSoup(entry.summary, 'html.parser')
            news.content = content.text
        except AttributeError:
            script_logger.warning('Current article has no content.')
            news.content = 'This article has no content.'
        try:
            news.images = entry.media_content[0]['url']
        except AttributeError:
            script_logger.warning('Current article has no images.')
            news.images = 'This article has no images.'
        try:
            news.rss_link = thefeed.feed.title_detail.get('base', '')
        except AttributeError:
            script_logger.warning('Current article has no \'rss_link\' key.')
            news.rss = 'This article has no rss_link.'
        news.source = thefeed.feed.get('link', '')
        news_list.append(news)
    script_logger.info('List of news was created successfully.')
    return news_list


def limit_news_list(news_list, args, script_logger):
    script_logger.info('Creating limit list of news entries.....')
    if not limit_arg_check(args, script_logger):
        script_logger.info('List of news was created successfully.')
        return news_list
    else:
        if args.limit == 0:
            script_logger.info('List of news was created successfully.')
            return news_list
        limit = args.limit
    if len(news_list) < limit:
        script_logger.warning('The number of news is less than --limit argument value.')
        return news_list
    news_list = news_list[:limit]
    script_logger.info('Limit list of news was created successfully.')
    return news_list


def output(news_list, thefeed, script_logger):
    """Output news."""
    script_logger.info('Please, read news.')
    print('-' * 120)
    print('Feed: ', thefeed.feed.get('title', ''))
    print('-' * 120)
    for news in news_list:
        news.outputing()


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
                ],
                'Source': news.source,
                'Images': news.images
             }
        }
        news_list_json.append(news_dict)
    script_logger.info('Please, read news in json format.')
    for news in news_list_json:
        print('-' * 120)
        print(json.dumps(news, indent=4, ensure_ascii=False))


def print_version(script_logger):
    """Simply prints version of rss_reader.py script."""
    script_logger.info('Check program version.....')
    version = 'rss_reader, version 2.0'
    return version


def convert_date(str_date):
    """Converting date function."""
    try:
        datetime_obj = datetime.strptime(str_date, '%Y%m%d')
        str_date = datetime_obj.strftime("%d %b %Y")
        if str_date[0] == '0':
            str_date = str_date[1:]
        return str_date
    except Exception:
        raise Error('Input correct date argument')

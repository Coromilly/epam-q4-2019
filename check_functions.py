"""This module contains different checks."""
import requests
import feedparser


class Error(Exception):
    """Class to raise own exceptions."""
    pass


def internet_connection_check(script_logger):
    """Check internet connection."""
    try:
        script_logger.info("Checking internet connection.....")
        requests.get('http://google.com', timeout=5)
    except requests.exceptions.ConnectionError:
        script_logger.error("No internet connection.")
        raise Error('Check your internet connection and try again.')
    else:
        script_logger.info("You have an internet connection.")


def url_check(args, script_logger):
    """Check URL from 'source' argument/"""
    try:
        script_logger.info('Url format check.....')
        thefeed = feedparser.parse(args.source)
        if 'title' in thefeed.feed:
            requests.get(args.source)
        else:
            raise Error
    except Error:
        script_logger.info('Wrong \'source\' argument.')
        raise Error('Check the link you have passed.')
    except requests.URLRequired:
        script_logger.info('A valid URL is required to make a request.')
        raise Error('Wrong link was passed.')
    except requests.HTTPError:
        script_logger.info('A Connection error occurred.')
        raise Error('Troubles with access to source.')
    else:
        script_logger.info('Url format is correct.')


def news_list_check(news_list, script_logger):
    """Check if news list has entries(news objects)."""
    script_logger.info('Checking news list emptiness.....')
    if not news_list:
        script_logger.error('The source you provided has no rss-content.')
        raise Error('Check url and try again.')
    else:
        script_logger.info('News list is not empty.')


def limit_arg_check(args, script_logger):
    """Check the --limit argument."""
    script_logger.info('Checking --limit argument.....')
    limit = args.limit
    if not limit:
        if limit == 0:
            script_logger.warning('Warning: --limit argument is 0, all news will be printed.')
            return True
        else:
            script_logger.error('Argument --limit has no value.')
            raise Error('Argument --limit: expected one int value.')
    elif args.limit < 0:
        script_logger.error('Argument --limit takes only positive values.')
        raise Error('Argument --limit should be positive.')
    else:
        return True

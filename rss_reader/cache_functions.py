"""Module of caching functions.

Functions:
caching_news returns None
getting_cached_news_list returns news_list
"""
from check_functions import Error, limit_arg_check
from os import path
import shelve


directory = path.abspath(path.dirname(__file__))
path_to_file = path.join(directory, '.cached_rss_news')


def caching_news(news_list, script_logger):
    """ Caching news function. """
    script_logger.info('Adding cached news to file.....')
    with shelve.open(path_to_file) as news_dict:
        for news in news_list:
            date_key = news.date
            news_dict[date_key] = news
    script_logger.info('RSS-news were cached successfully.')


def getting_cached_news_list(args, script_logger):
    script_logger.info('Getting cached news.....')
    news_list = []
    with shelve.open(path_to_file) as shelve_dict:
        if not shelve_dict:
            raise Error('There are no cached news. You can read news from internet if the connection exists.')
        if not limit_arg_check(args, script_logger):
            limit = len(shelve_dict)
        elif args.limit == 0:
            limit = len(shelve_dict)
        else:
            limit = min(args.limit, len(shelve_dict))
        for date_key in shelve_dict:
            if args.date in date_key:
                news = shelve_dict[date_key]
                if args.source == news.rss_link:
                    news_list.append(news)
                else:
                    script_logger.error('There are no cached news for this link.')
                    raise Error('Wrong link.')
    if not news_list:
        script_logger.error('There are no news in cached file at this date and source.')
        raise Error('There are no news in cached file. Input another date or source.')
    else:
        script_logger.info('News were got successfully from cache.')
        return news_list[:limit]

"""  Module of caching functions.
      Functions:
      cache_news(news_collection, logger) -> None
      get_cached_news(com_line_args, logger) -> cached_news_collection   """

import shelve
from os import path

from check_functions import Error, limit_arg_check

DIRECTORY = path.abspath(path.dirname(__file__))
path_to_file = path.join(DIRECTORY, '.cached_rss_news')


def caching_news(news_list, script_logger):
    """ Caching news function. """
    script_logger.info('Adding cached news to file.....')
    with shelve.open(path_to_file) as news_dict:
        for news in news_list:
            date_key = news.date
            news_dict[date_key] = news
    script_logger.info('RSS-news were cached successfully.')


def getting_cached_news_list(date, args, script_logger):
    script_logger.info('Getting cached news.....')
    news_list = []
    with shelve.open(path_to_file) as shelve_dict:
        if not shelve_dict:
            raise Error('There are no cached news. You can read news from internet if the connection exists.')
        if not limit_arg_check(args, script_logger):
            limit = len(shelve_dict)
        else:
            limit = min(args.limit, len(shelve_dict))
        for date_key in shelve_dict:
            if date in date_key:
                news = shelve_dict[date_key]
                # if args.source == news.source:
                news_list.append(news)
    if not news_list:
        script_logger.error('There are no news in cached file at this date and source.')
        raise Error('There are no news in cached file. Input another date or source.')
    else:
        script_logger.info('News were got successfully from cache.')
        return news_list[:limit]

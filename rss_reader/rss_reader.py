"""This is module rss_reader.py version 1.

Usage in CLI:
>python rss_reader.py source [-h] [--version] [--json] [--verbose] [--limit LIMIT]

positional arguments:
  source         RSS URL

optional arguments:
  -h, --help     show this help message and exit
  --version      Print version info
  --json         Print result as JSON in stdout
  --verbose      Outputs verbose status messages
  --limit LIMIT  Limit news topics if this parameter provided
"""
from cache_functions import caching_news, getting_cached_news_list
from check_functions import Error, internet_connection_check, limit_arg_check
from check_functions import news_list_check, url_check
from main_functions import logger, getting_arguments, getting_feed, creating_news_list
from main_functions import limit_news_list, output, output_in_json, print_version


def main():
    try:
        args = getting_arguments()
        script_logger = logger(args)
        thefeed = getting_feed(args, script_logger)
        if args.version:
            print(print_version(script_logger))
        else:
            if args.date:
                news_list = getting_cached_news_list(args, script_logger)
                if args.json:
                    output_in_json(news_list, thefeed, script_logger)
                else:
                    output(news_list, thefeed, script_logger)
            else:
                internet_connection_check(script_logger)
                url_check(args, script_logger)
                if limit_arg_check(args, script_logger):
                    news_list = creating_news_list(thefeed, script_logger)
                    news_list_check(news_list, script_logger)
                    caching_news(news_list, script_logger)
                    lim_news_lst = limit_news_list(news_list, args, script_logger)
                    if args.json:
                        output_in_json(lim_news_lst, thefeed, script_logger)
                    else:
                        output(lim_news_lst, thefeed, script_logger)
                else:
                    news_list = creating_news_list(thefeed, script_logger)
                    news_list_check(news_list, script_logger)
                    if args.json:
                        output_in_json(news_list, thefeed, script_logger)
                    else:
                        output(news_list, thefeed, script_logger)
    except Error as e:
        print(e)


if __name__ == '__main__':
    main()

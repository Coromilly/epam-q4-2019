from rss_reader import *


def main():
    args = getting_arguments()
    script_logger = logger(args)
    if args.version:
        print_version(script_logger)
    else:
        thefeed = getting_feed(args, script_logger)
        news_list = creating_news_list(thefeed, script_logger)
        if args.limit:
            news_lst = limit_news_list(news_list, args, script_logger)
            if args.json:
                output_in_json(news_lst, thefeed, script_logger)
            else:
                output(news_lst, thefeed, script_logger)
        else:
            output(news_list, thefeed, script_logger)


if __name__ == '__main__':
    main()

from main_functions import *
from check_functions import *


def main():
    try:
        args = getting_arguments()
        script_logger = logger(args)
        if args.version:
            print(print_version(script_logger))
        else:
            internet_connection_check(script_logger)
            url_check(args, script_logger)
            if limit_arg_check(args, script_logger):
                thefeed = getting_feed(args, script_logger)
                news_list = creating_news_list(thefeed, script_logger)
                news_list_check(news_list, script_logger)
                lim_news_lst = limit_news_list(news_list, args, script_logger)
                if args.json:
                    output_in_json(lim_news_lst, thefeed, script_logger)
                else:
                    output(lim_news_lst, thefeed, script_logger)
            else:
                thefeed = getting_feed(args, script_logger)
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

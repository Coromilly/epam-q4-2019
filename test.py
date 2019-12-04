from rss_reader import *


def main():
    args = getting_arguments()
    thefeed = getting_feed(args)
    news_list = creating_list_of_entries(thefeed)
    # output(args, thefeed, news_list)
    convert_to_json(news_list, args, thefeed)


if __name__ == '__main__':
    main()

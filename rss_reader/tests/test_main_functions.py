"""This module contains unit tests for main functions."""
from check_functions import Error
import feedparser
import main_functions
import unittest
from unittest.mock import Mock, patch


class TestClassContent(unittest.TestCase):
    """Here is tested class method 'Content__init__' from 'main_functions' module."""

    def setUp(self):
        self.A = main_functions.Content()
        self.A.title = 'title'
        self.A.date = ['date', 1]
        self.A.link = {2: 'link'}
        self.A.content = []
        self.A.source = 'https://www.yahoo.com/news'
        self.A.rss_link = 'https://news.yahoo.com/rss/'
        self.A.images = (1, 'f')

    def test_class_content_init(self):
        self.assertEqual(self.A.title, 'title')
        self.assertEqual(self.A.date, ['date', 1])
        self.assertEqual(self.A.link, {2: 'link'})
        self.assertEqual(self.A.content, [])
        self.assertEqual(self.A.source, 'https://www.yahoo.com/news')
        self.assertEqual(self.A.rss_link, 'https://news.yahoo.com/rss/')
        self.assertEqual(self.A.images, (1, 'f'))


class TestMainFunctions(unittest.TestCase):
    """Here are tested some functions from 'main_functions.py' module."""

    def setUp(self):
        self.script_logger = Mock()
        self.args = Mock()

    def test_limit_news_list(self):
        news_list = [1, 2, 3, 4, 5]
        self.args.limit = 2
        self.assertEqual(len(main_functions.limit_news_list(news_list, self.args, self.script_logger)), 2)
        self.args.limit = 10
        self.assertEqual(len(main_functions.limit_news_list(news_list, self.args, self.script_logger)), 5)
        self.args.limit = 0
        self.assertEqual(len(main_functions.limit_news_list(news_list, self.args, self.script_logger)), 5)

    def test_print_version(self):
        self.assertEqual(main_functions.print_version(self.script_logger), 'rss_reader, version 2.0')

    def test_getting_feed(self):
        with patch('feedparser.parse') as parser_mock:
            parser_mock.return_value = 5
            self.assertEqual(main_functions.getting_feed(self.args, self.script_logger), 5)

    def test_creating_news_list(self):
        feed = """<?xml version="1.0" encoding="utf-8" ?>
            <rss version="2.0">
            <channel>
            <title>feed</title>
            <item>
            <title>title</title>
            <link>link</link>
            <description>content</description>
            <pubDate>date</pubDate>
            </item>
            </channel>
            </rss>
        """
        thefeed = feedparser.parse(feed)
        news_list = main_functions.creating_news_list(thefeed, self.script_logger)
        self.assertEqual(len(news_list), 1)

    def test_convert_date(self):
        self.assertEqual(main_functions.convert_date("20191211"), "11 Dec 2019")
        self.assertEqual(main_functions.convert_date("20190205"), "5 Feb 2019")
        with self.assertRaises(Error):
            main_functions.convert_date("2119")


if __name__ == '__main__':
    unittest.main()

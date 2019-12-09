"""This module contains unit tests.

Functions from module 'main_functions.py' are tested in class 'TestMainFunctions'.
Functions from module 'check_functions.py' are tested in class 'TestCheckFunctions'.
"""
import check_functions
from contextlib import redirect_stdout
import feedparser
import io
import main_functions
import requests
import sys
import unittest
from unittest import mock


class TestClassContent(unittest.TestCase):

    def setUp(self):
        self.A = main_functions.Content()
        self.A.title = 'title'
        self.A.date = '09.12.2019'
        self.A.link = 'link'
        self.A.content = 'content'

    def test_class_content_init(self):
        self.assertEqual(self.A.title, 'title')
        self.assertEqual(self.A.date, '09.12.2019')
        self.assertEqual(self.A.link, 'link')
        self.assertEqual(self.A.content, 'content')



class TestMainFunctions(unittest.TestCase):
    """Here are tested some functions from 'main_functions.py' module."""

    def setUp(self):
        self.script_logger = mock.Mock()
        self.args = mock.Mock()

    def test_limit_news_list(self):
        news_list = [1, 2, 3, 4, 5]
        self.args.limit = 2
        self.assertEqual(len(main_functions.limit_news_list(news_list, self.args, self.script_logger)), 2)
        self.args.limit = 10
        self.assertEqual(len(main_functions.limit_news_list(news_list, self.args, self.script_logger)), 5)
        self.args.limit = 0
        self.assertEqual(len(main_functions.limit_news_list(news_list, self.args, self.script_logger)), 5)

    def test_print_version(self):
        self.assertEqual(main_functions.print_version(self.script_logger), 'rss_reader, version 1.0')

    def test_getting_feed(self):
        with mock.patch('feedparser.parse') as parser_mock:
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


class TestCheckFunctions(unittest.TestCase):
    """Here are tested some functions from 'check_functions.py' module."""

    def setUp(self):
        self.script_logger = mock.Mock()
        self.args = mock.Mock()

    def test_internet_connection_check(self):
        with mock.patch('requests.get'):
            self.assertTrue(check_functions.internet_connection_check(self.script_logger))
        with self.assertRaises(check_functions.Error):
            with mock.patch('requests.get', side_effect=requests.exceptions.ConnectionError):
                check_functions.internet_connection_check(self.script_logger)

    def test_url_check(self):
        with mock.patch('requests.get'):
            self.assertTrue(check_functions.url_check(self.args, self.script_logger))
        with self.assertRaises(check_functions.Error):
            with mock.patch('requests.get', side_effect=requests.exceptions.MissingSchema):
                check_functions.url_check(self.args, self.script_logger)
        with self.assertRaises(check_functions.Error):
            with mock.patch('requests.get', side_effect=requests.exceptions.InvalidSchema):
                check_functions.url_check(self.args, self.script_logger)
        with self.assertRaises(check_functions.Error):
            with mock.patch('requests.get', side_effect=requests.HTTPError):
                check_functions.url_check(self.args, self.script_logger)

    def test_news_list_check(self):
        with self.assertRaises(check_functions.Error):
            news_list = []
            check_functions.news_list_check(news_list, self.script_logger)
        news_list = [1, 'two', {3: 'three'}]
        self.assertTrue(check_functions.news_list_check(news_list, self.script_logger))

    def test_limit_arg_check(self):
        self.args.limit = 0
        self.assertTrue(check_functions.limit_arg_check(self.args, self.script_logger))
        self.args.limit = []
        self.assertFalse(check_functions.limit_arg_check(self.args, self.script_logger))
        self.args.limit = None
        self.assertFalse(check_functions.limit_arg_check(self.args, self.script_logger))
        self.args.limit = 5
        self.assertTrue(check_functions.limit_arg_check(self.args, self.script_logger))
        with self.assertRaises(check_functions.Error):
            self.args.limit = -1
            check_functions.limit_arg_check(self.args, self.script_logger)


if __name__ == '__main__':
    unittest.main()

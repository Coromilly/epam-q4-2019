"""This module contains unit tests for check functions."""
import check_functions
import requests
import unittest
from unittest.mock import Mock, patch


class TestCheckFunctions(unittest.TestCase):
    """Here are tested some functions from 'check_functions.py' module."""

    def setUp(self):
        self.script_logger = Mock()
        self.args = Mock()

    def test_internet_connection_check(self):
        with patch('requests.get'):
            self.assertTrue(check_functions.internet_connection_check(self.script_logger))
        with self.assertRaises(check_functions.Error):
            with patch('requests.get', side_effect=requests.exceptions.ConnectionError):
                check_functions.internet_connection_check(self.script_logger)

    def test_url_check(self):
        with patch('requests.get'):
            self.assertTrue(check_functions.url_check(self.args, self.script_logger))
        with self.assertRaises(check_functions.Error):
            with patch('requests.get', side_effect=requests.exceptions.MissingSchema):
                check_functions.url_check(self.args, self.script_logger)
        with self.assertRaises(check_functions.Error):
            with patch('requests.get', side_effect=requests.exceptions.InvalidSchema):
                check_functions.url_check(self.args, self.script_logger)
        with self.assertRaises(check_functions.Error):
            with patch('requests.get', side_effect=requests.HTTPError):
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

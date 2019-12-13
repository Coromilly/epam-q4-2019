"""This module contains unit tests for caching functions."""
import cache_functions
import check_functions
import main_functions
import os
import unittest
from unittest import mock

A = main_functions.Content()
A.title = 'Texas inmate executed for killing prison supervisor in 2003'
A.date = 'Wed, 11 Dec 2019 00:03:58 -0500'
A.link = 'https://news.yahoo.com/texas-inmate-faces-execution-killing-050358562.html'
A.content = '''A Texas inmate was executed by lethal injection Wednesday evening for killing a 
        supervisor at a state prison shoe factory in Amarillo nearly 17 years ago.  Travis Runnels, 46, 
        was convicted of slashing the throat of 38-year-old Stanley Wiley on Jan. 29, 2003.  Runnels was 
        executed at the state penitentiary in Huntsville.'''
A.source = 'https://www.yahoo.com/news'
A.rss_link = 'https://news.yahoo.com/rss/'

B = main_functions.Content()
B.title = 'Barr contradicts his own inspector general: Trump campaign \'was clearly spied upon\''
B.date = 'Tue, 10 Dec 2019 14:44:49 -0500'
B.link = 'https://news.yahoo.com/barr-contradicts-his-own-inspector-general-' \
         'trump-campaign-was-clearly-spied-upon-194449546.html'
B.content = '''Attorney General William Barr sharply contradicted the findings of a 
        report by the inspector general on the origins of the Mueller report on the Trump 
        campaign's ties to Russia.'''
B.source = 'https://www.yahoo.com/news'
B.rss_link = 'https://news.yahoo.com/rss/'
B.images = ['link1']
news_list = [A, B]
directory = os.path.abspath(os.path.dirname(__file__))


class TestCacheFunctions(unittest.TestCase):
    """Here are tested some functions from 'cache_functions.py' module."""

    def setUp(self):
        self.A = A
        self.B = B
        self.news_list = news_list
        self.script_logger = mock.Mock()
        self.args = mock.Mock()
        self.home_dir = os.path.expanduser('~')
        self.test_file_path = os.path.join(directory, '.test_cache_rss_news')
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)

    @mock.patch('os.path.join')
    def test_getting_cached_news_list(self, path):
        path.return_value = self.test_file_path
        cache_functions.caching_news(self.news_list, self.script_logger)

        self.args.limit = 3
        self.args.date = '15 Dec 2019'
        self.args.source = 'https://news.yahoo.com/rss/'
        with self.assertRaises(check_functions.Error):
            cache_functions.getting_cached_news_list(self.args, self.script_logger)

        self.args.date = '10 Dec 2019'
        self.args.source = 'https://www.espn.com/espn/rss/mlb/news'
        with self.assertRaises(check_functions.Error):
            cache_functions.getting_cached_news_list(self.args, self.script_logger)

        self.args.date = '11 Dec 2019'
        self.args.source = 'https://news.yahoo.com/rss/'
        news_collection = cache_functions.getting_cached_news_list(self.args, self.script_logger)
        num_of_news = len(news_collection)
        self.assertEqual(num_of_news, 1)
        news_title = 'Texas inmate executed for killing prison supervisor in 2003'
        self.assertEqual(news_collection[0].title, news_title)

        self.args.date = '10 Dec 2019'
        self.args.source = ''
        with self.assertRaises(check_functions.Error):
            cache_functions.getting_cached_news_list(self.args, self.script_logger)


if __name__ == '__main__':
    unittest.main()

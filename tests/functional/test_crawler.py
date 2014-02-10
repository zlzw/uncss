from unittest import TestCase
from uncss.crawler import StaticContentCrawler, DynamicContentCrawler, UnknownHostException, NotSuccessException,\
    PhantomjsCannotBeFoundException, ScriptCannotBeFoundException
import os


class StaticContentCrawlerTestCase(TestCase):
    def setUp(self):
        self.crawler = StaticContentCrawler()

    def test_get_source_ok(self):
        html = self.crawler.get_source('http://www.example.com')
        self.assertTrue("<title>Example Domain</title>" in html)

    def test_get_source_invalid_domain(self):
        self.assertRaises(UnknownHostException, self.crawler.get_source, 'http://www.fakedomain12345678abcdefgh12345.com')

    def test_get_source_not_success(self):
        self.assertRaises(NotSuccessException, self.crawler.get_source, 'http://www.google.com/404')


class DynamicContentCrawlerTestCase(TestCase):
    def setUp(self):
        self.crawler = DynamicContentCrawler()

    def test_phantomjs_cannot_be_found(self):
        self.assertRaises(PhantomjsCannotBeFoundException, DynamicContentCrawler, 'badphantomjs')

    def test_get_source_ok(self):
        html = self.crawler.get_source('http://www.example.com')
        self.assertTrue("<title>Example Domain</title>" in html)

    def test_absolute_script_file_path_get_source_ok(self):
        current_path = os.path.dirname(os.path.realpath(__file__))
        absolute_script_file_path = os.path.abspath("%s/../../uncss/phantomjs_get_source.js" % current_path)
        self.crawler = DynamicContentCrawler()
        html = self.crawler.get_source('http://www.example.com', absolute_script_file_path)
        self.assertTrue("<title>Example Domain</title>" in html)

    def test_relative_script_file_path_not_found(self):
        relative_script_file_path = "../invalid_phantomjs_get_source.js"
        self.crawler = DynamicContentCrawler()

        get_source_args = {
            'url': 'http://www.example.com',
            'script_file_path': relative_script_file_path
        }

        self.assertRaises(ScriptCannotBeFoundException, self.crawler.get_source, *get_source_args)

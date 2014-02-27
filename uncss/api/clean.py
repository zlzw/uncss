from apy.application import Controller
from apy.http import JsonResponse, Response
from uncss.crawler import StaticContentCrawler
from uncss.resources import HtmlResource, CssResource
from uncss.processor import CssCleaner
from redis import StrictRedis
import hashlib
from abc import abstractmethod, ABCMeta
import os.path

try:
    # python 3
    from urllib.parse import unquote
except ImportError:
    # python 2
    from urllib import unquote


class SourceManager(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def save(self, source):
        pass

    @abstractmethod
    def load(self, identification):
        pass


class RedisSourceManager(SourceManager):
    def __init__(self, prefix):
        self.redis = StrictRedis()
        self.prefix = prefix

    def save(self, source):
        identification = hashlib.md5(source.encode('utf-8')).hexdigest()
        if not self.redis.exists('%s:%s' % (self.prefix, identification)):
            self.redis.set(('%s:%s' % (self.prefix, identification)), source)
        return identification

    def load(self, identification):
        source = self.redis.get('%s:%s' % (self.prefix, identification))
        return str(source, encoding='UTF-8')  # TODO: fix this. (doesn't work on python 2)


class FileSourceManager(SourceManager):
    def __init__(self, path):
        self.path = path.rstrip('/')
        if not os.path.exists(path):
            os.makedirs(path)

    def save(self, source):
        identification = hashlib.md5(source.encode('utf-8')).hexdigest()
        file_name = '%s/%s' % (self.path, identification)
        if not os.path.isfile(file_name):
            f = open(file_name, 'wb')
            source = source.encode('utf-8')
            f.write(source)
            f.close()

        return identification

    def load(self, identification):
        file_name = '%s/%s' % (self.path, identification)
        source = open(file_name, 'rb').read()
        source = source.decode(encoding='utf-8')
        return source


class CleanController(Controller):
    def post_controller(self, response):
        response.headers.add(
            {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept'
            }
        )
        return response


class ProcessHtml(CleanController):
    def validate_action(self):
        if not self._request.data.has('url'):
            return False

    def action(self):
        url = self._request.data.get('url')

        url = unquote(url)

        response = JsonResponse()

        content_crawler = StaticContentCrawler()

        html_source = content_crawler.get_source(url)
        html_resource = HtmlResource(html_source, url)
        links = html_resource.get_external_css_urls()

        html_manager = FileSourceManager('/tmp/uncss/html')
        html_key = html_manager.save(html_source)

        response.data = {
            'links': links,
            'html_key': html_key
        }

        return response


class CleanCss(CleanController):
    def action(self):
        html_key = self._request.data.get('html_key')
        css_source_url = self._request.data.get('css_source_url')

        css_source_url = unquote(css_source_url)

        html_manager = FileSourceManager('/tmp/uncss/html')
        html_source = html_manager.load(html_key)

        content_crawler = StaticContentCrawler()
        css_source = content_crawler.get_source(css_source_url)
        css_resource = CssResource(css_source)
        css_cleaner = CssCleaner(html_source, [css_resource])  # TODO: fix the unicode html_source -> str
        cleaned_css_resources = css_cleaner.clean_css_resources()
        cleaned_css_resource = cleaned_css_resources[0]
        cleaned_css_source = cleaned_css_resource.get_as_string()

        css_manager = FileSourceManager('/tmp/uncss/css')
        css_key = css_manager.save(cleaned_css_source)

        response = Response()

        response.data = css_key

        return response


class GetCss(CleanController):
    def action(self, css_key):
        css_manager = FileSourceManager('/tmp/uncss/css')
        css_source = css_manager.load(css_key)

        response = Response()

        response.data = css_source

        return response

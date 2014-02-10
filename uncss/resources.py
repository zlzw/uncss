from lxml import etree
from lxml.cssselect import CSSSelector
import cssutils

try:
    # python 3
    from urllib.parse import urljoin
except ImportError:
    # python 2
    from urlparse import urljoin


class HtmlResource:
    def __init__(self, html_source, base_url):
        """
        @type html_source str
        @type base_url str
        """
        parser = etree.HTMLParser(encoding='utf-8')
        tree = etree.fromstring(html_source.encode('utf-8'), parser).getroottree()
        self.html_page = tree.getroot()
        self.base_url = base_url

    def get_external_css_urls(self):
        urls = []
        for link in CSSSelector('link')(self.html_page):
            if self.__is_link_css(link):
                link_url = self.make_absolute_url(self.base_url, link.attrib['href'])
                urls.append(link_url)

        return urls

    @staticmethod
    def __is_link_css(link):
        return link.attrib.get('rel', '') == 'stylesheet' or link.attrib['href'].lower().split('?')[0].endswith('.css')

    @staticmethod
    def make_absolute_url(url, href):
        """
        @type url str
        @type href str
        """
        return urljoin(url, href)


class CssResource:
    def __init__(self, css_source=None, url=None):
        """
        @type css_source str or None
        @type url str or None
        """
        self.rules = self._get_rules(css_source) if css_source else None
        self.url = url

    @staticmethod
    def _get_rules(css_source):
        rules = []
        sheet = cssutils.parseString(css_source)

        for rule in sheet:
            selectors = []
            selector_list = rule.selectorList.seq
            for selector in selector_list:
                selector_name = selector.selectorText
                selectors.append(selector_name)
            styles = rule.style.cssText
            rules.append((selectors, styles))

        return rules

    def __str__(self):
        string = ''
        for rule in enumerate(self.rules):
            key = ', '.join(rule[1][0])
            string += "%s {\n%s\n}\n" % (key, rule[1][1])

        return string

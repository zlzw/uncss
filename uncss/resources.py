from lxml import etree
from lxml.cssselect import CSSSelector
import cssutils
import logging
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
        if base_url[:7] != "http://" and base_url[:8] != "https://":
            base_url = 'http://' + base_url
        self.base_url = base_url

    def get_external_css_urls(self):
        urls = []
        for link in CSSSelector('link')(self.html_page):
            link_url = link.attrib['href']
            if self.__is_link_css(link):
                link_url = self.make_absolute_url(self.base_url, link_url)
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
        self.non_rules = []
        self.rules = []
        self.url = url

        if css_source is not None:
            self._extract_styles(css_source)

    def _extract_styles(self, css_source):
        cssutils.log.setLevel(logging.CRITICAL)
        sheet = cssutils.parseString(css_source, validate=False)

        for style in sheet:
            if isinstance(style, cssutils.css.CSSStyleRule):
                selectors = []
                selector_list = style.selectorList.seq
                for selector in selector_list:
                    selector_name = selector.selectorText
                    selectors.append(selector_name)
                styles = style.style.cssText
                self.rules.append((selectors, styles))
            elif not isinstance(style, cssutils.css.CSSComment):
                self.non_rules.append(style.cssText)

    def get_as_string(self):
        string = ''
        for rule in enumerate(self.rules):
            key = ', '.join(rule[1][0])
            string += "%s {\n%s\n}\n" % (key, rule[1][1])

        for non_rule in self.non_rules:
            string += "%s\n" % non_rule

        return string

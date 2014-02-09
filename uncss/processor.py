from lxml import etree
from lxml.cssselect import CSSSelector
import cssutils


class CssResource:
    def __init__(self, css_source=None, url=None):
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

class CssCleaner:
    SPECIAL_SELECTORS = ['html']

    def __init__(self, html, css_resources, preserve_special_selectors=True):
        """
        @type html str
        @type css_resources CssResource()[]
        """
        self.body = self._get_body_from_html(html)
        self.css_resources = css_resources
        self.preserve_special_selectors = preserve_special_selectors

    @staticmethod
    def _get_body_from_html(html):
        """ @type html str """
        parser = etree.HTMLParser(encoding='utf-8')
        tree = etree.fromstring(html.encode('utf-8'), parser).getroottree()
        page = tree.getroot()

        return CSSSelector('body')(page)[0]

    def clean_css_resources(self):
        cleaned_css_resources = []
        for css_resource in self.css_resources:
            cleaned_css_resources.append(self._clean_css_resource(css_resource))
        return cleaned_css_resources

    def _clean_css_resource(self, css_resource):
        """ @type css_resource CssResource() """
        used_rules = []
        for rule in css_resource.rules:
            used_selectors = []
            selectors = rule[0]
            for selector in selectors:
                if self._is_used_selector(selector):
                    used_selectors.append(selector)
            if used_selectors:
                used_rules.append((used_selectors, rule[1]))

        cleaned_css_resource = CssResource(url=css_resource.url)
        cleaned_css_resource.rules = used_rules

        return cleaned_css_resource

    def _is_used_selector(self, selector):
        """ @type selector str """
        if self.preserve_special_selectors and selector in self.SPECIAL_SELECTORS:
            return True

        if CSSSelector(selector)(self.body):
            return True
        else:
            return False

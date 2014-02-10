from unittest import TestCase
from uncss.resources import HtmlResource, CssResource


HTML_SOURCE = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>one</title>
        <link rel="stylesheet" href='one.css'>
        <link rel="stylesheet" href='two/foo.css'>
        <link rel="stylesheet" href='http://www.example.com/two.css'>
    </head>
    <body>
        <h1>h1</h1>
        <h2>h2</h2>
        <h3>h3</h3>
    </body>
    </html>
"""

CSS_SOURCE = """
    body, html { margin: 0; }
    h1, h2, h3 { text-align: center; }
    h3, h4 { font-family: serif; }
    .foo { something:hello }
    .foo, h4, h2 { color:red }
    #none, .hello { world: hello; }
"""


class HtmlResourceTestCase(TestCase):
    def test_get_external_css_urls(self):
        html_resource = HtmlResource(HTML_SOURCE, 'http://example.com')
        external_css_urls = html_resource.get_external_css_urls()
        self.assertEqual(
            ['http://example.com/one.css', 'http://example.com/two/foo.css', 'http://www.example.com/two.css'],
            external_css_urls
        )


class CssResourceTestCase(TestCase):
    def test_rules(self):
        css_resource = CssResource(CSS_SOURCE)

        expected_rules = [
            (['body', 'html'], 'margin: 0'),
            (['h1', 'h2', 'h3'], 'text-align: center'),
            (['h3', 'h4'], 'font-family: serif'),
            (['.foo'], 'something: hello'),
            (['.foo', 'h4', 'h2'], 'color: red'),
            (['#none', '.hello'], 'world: hello')
        ]

        self.assertEqual(expected_rules, css_resource.rules)

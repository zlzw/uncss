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
    @font-face {
      font-family: 'News Cycle';
      font-style: normal;
      font-weight: 400;
      src: local('News Cycle Regular'), local('NewsCycle-Regular'), url(http://themes.googleusercontent.com/static/fonts/newscycle/v10/9Xe8dq6pQDsPyVH2D3tMQr3hpw3pgy2gAi-Ip7WPMi0.woff) format('woff');
    }
    @font-face {
      font-family: 'News Cycle';
      font-style: normal;
      font-weight: 700;
      src: local('News Cycle Bold'), local('NewsCycle-Bold'), url(http://themes.googleusercontent.com/static/fonts/newscycle/v10/G28Ny31cr5orMqEQy6ljt3bFhgvWbfSbdVg11QabG8w.woff) format('woff');
    }

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

    def test_base_url_without_http_https(self):
        html_resource = HtmlResource(HTML_SOURCE, 'example.com')
        self.assertEqual('http://example.com', html_resource.base_url)


class CssResourceTestCase(TestCase):
    def setUp(self):
        self.css_resource = CssResource(CSS_SOURCE)

    def test_rules(self):
        expected_rules = [
            (['body', 'html'], 'margin: 0'),
            (['h1', 'h2', 'h3'], 'text-align: center'),
            (['h3', 'h4'], 'font-family: serif'),
            (['.foo'], 'something: hello'),
            (['.foo', 'h4', 'h2'], 'color: red'),
            (['#none', '.hello'], 'world: hello')
        ]

        self.assertEqual(expected_rules, self.css_resource.rules)

    def test_non_rules(self):
        expected_non_rules = [
            """@font-face {
    font-family: "News Cycle";
    font-style: normal;
    font-weight: 400;
    src: local("News Cycle Regular"), local("NewsCycle-Regular"), url(http://themes.googleusercontent.com/static/fonts/newscycle/v10/9Xe8dq6pQDsPyVH2D3tMQr3hpw3pgy2gAi-Ip7WPMi0.woff) format("woff")
    }""",
            """@font-face {
    font-family: "News Cycle";
    font-style: normal;
    font-weight: 700;
    src: local("News Cycle Bold"), local("NewsCycle-Bold"), url(http://themes.googleusercontent.com/static/fonts/newscycle/v10/G28Ny31cr5orMqEQy6ljt3bFhgvWbfSbdVg11QabG8w.woff) format("woff")
    }"""
        ]

        self.assertEqual(expected_non_rules, self.css_resource.non_rules)

    def test_to_str(self):
        expected_css_as_string = """body, html {
margin: 0
}
h1, h2, h3 {
text-align: center
}
h3, h4 {
font-family: serif
}
.foo {
something: hello
}
.foo, h4, h2 {
color: red
}
#none, .hello {
world: hello
}
@font-face {
    font-family: "News Cycle";
    font-style: normal;
    font-weight: 400;
    src: local("News Cycle Regular"), local("NewsCycle-Regular"), url(http://themes.googleusercontent.com/static/fonts/newscycle/v10/9Xe8dq6pQDsPyVH2D3tMQr3hpw3pgy2gAi-Ip7WPMi0.woff) format("woff")
    }
@font-face {
    font-family: "News Cycle";
    font-style: normal;
    font-weight: 700;
    src: local("News Cycle Bold"), local("NewsCycle-Bold"), url(http://themes.googleusercontent.com/static/fonts/newscycle/v10/G28Ny31cr5orMqEQy6ljt3bFhgvWbfSbdVg11QabG8w.woff) format("woff")
    }
"""
        css_as_string = self.css_resource.get_as_string()
        self.assertEqual(expected_css_as_string, css_as_string)


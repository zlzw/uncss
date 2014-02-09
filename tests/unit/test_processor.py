from unittest import TestCase
from uncss.processor import CssResource, CssCleaner


HTML_SOURCE = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>one</title>
        <link rel="stylesheet" href='one.css'>
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


class ProcessorTestCase(TestCase):
    def setUp(self):
        css_resources = [CssResource(CSS_SOURCE)]
        self.processor = CssCleaner(HTML_SOURCE, css_resources)

    def test_clean_css_resources(self):
        cleaned_css_resources = self.processor.clean_css_resources()

        expected_cleaned_css_resources = [
            (['body', 'html'], 'margin: 0'),
            (['h1', 'h2', 'h3'], 'text-align: center'),
            (['h3'], 'font-family: serif'),
            (['h2'], 'color: red')
        ]

        self.assertEqual(1, len(cleaned_css_resources))
        self.assertEqual(expected_cleaned_css_resources, cleaned_css_resources[0].rules)

    def test_clean_css_resources_and_dump(self):
        resources = self.processor.clean_css_resources()
        resource = resources[0]
        dump = str(resource)

        expected_dump = """body, html {
margin: 0
}
h1, h2, h3 {
text-align: center
}
h3 {
font-family: serif
}
h2 {
color: red
}
"""

        self.assertEqual(expected_dump, dump)

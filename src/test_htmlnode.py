import unittest

from htmlnode import HtmlNode


class TestTextNode(unittest.TestCase):
    def test_props_to_html(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HtmlNode(props=props)
        self.assertEqual(
            node.props_to_html(), " href=https://www.google.com target=_blank"
        )

    def test_init(self):
        props = {}
        tag = "p"
        children = []
        value = "value"
        node = HtmlNode(tag=tag, value=value, children=children, props=props)
        self.assertEqual(node.props, props)
        self.assertEqual(node.tag, tag)
        self.assertEqual(node.children, children)
        self.assertEqual(node.value, value)

    def test_init_none(self):
        node = HtmlNode()
        self.assertEqual(node.props, None)
        self.assertEqual(node.tag, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.value, None)

    def test_repr(self):
        tag = "p"
        value = "value"
        node = HtmlNode(tag=tag, value=value)
        self.assertEqual(repr(node), "HtmlNode(p, value, None, None)")


if __name__ == "__main__":
    unittest.main()

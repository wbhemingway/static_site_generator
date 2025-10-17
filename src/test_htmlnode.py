import unittest

from htmlnode import HtmlNode, LeafNode


class TestTextNode(unittest.TestCase):
    def test_props_to_html(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HtmlNode(props=props)
        self.assertEqual(
            node.props_to_html(), ' href="https://www.google.com" target="_blank"'
        )

    def test_props_to_html_none(self):
        props = {}
        node = HtmlNode(props=props)
        self.assertEqual(node.props_to_html(), "")

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


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )

    def test_leaf_no_value(self):
        def inner():
            node = LeafNode(None, None)
            return node.to_html()

        self.assertRaises(ValueError, inner)

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")


if __name__ == "__main__":
    unittest.main()

import unittest

from textnode import TextNode, TextType
from util import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_node_to_html_node,
    text_to_textnodes,
)


class TestTextToHtml(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href": "example.com"})

    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, "example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props, {"src": "example.com", "alt": "This is an image node"}
        )


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code(self):
        node = TextNode("This is a `code` block!", TextType.TEXT)
        expected_nodes = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" block!", TextType.TEXT),
        ]
        actual_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(actual_nodes, expected_nodes)

    def test_code_two(self):
        node = TextNode(
            "This is a `code` block with two `codey` sections!", TextType.TEXT
        )
        expected_nodes = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" block with two ", TextType.TEXT),
            TextNode("codey", TextType.CODE),
            TextNode(" sections!", TextType.TEXT),
        ]
        actual_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(actual_nodes, expected_nodes)

    def test_bold(self):
        node = TextNode("This is a **bold** block!", TextType.TEXT)
        expected_nodes = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" block!", TextType.TEXT),
        ]
        actual_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(actual_nodes, expected_nodes)

    def test_code_error(self):
        with self.assertRaises(Exception) as cm:
            node = TextNode("This is a `code block!", TextType.TEXT)
            actual_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
            return actual_nodes
        self.assertEqual(str(cm.exception), "No closing delimiter found for `")

    def test_code_error_one_valid(self):
        with self.assertRaises(Exception) as cm:
            node = TextNode("This is a `code` block`!", TextType.TEXT)
            actual_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
            return actual_nodes
        self.assertEqual(str(cm.exception), "No closing delimiter found for `")

    def test_starting_delimiter(self):
        node = TextNode("`This` is a `code` block!", TextType.TEXT)
        expected_nodes = [
            TextNode("This", TextType.CODE),
            TextNode(" is a ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" block!", TextType.TEXT),
        ]
        actual_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(actual_nodes, expected_nodes)

    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )


class TestExtractLinks(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_mult(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a second ![imagey](https://i.imgur.com/zjjcJasdaKZ.png)"
        )
        self.assertListEqual(
            [
                ("image", "https://i.imgur.com/zjjcJKZ.png"),
                ("imagey", "https://i.imgur.com/zjjcJasdaKZ.png"),
            ],
            matches,
        )

    def test_extract_markdown_link(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ)"
        )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ")], matches)

    def test_extract_markdown_link_mult(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ) and a second [linky](https://i.imgur.com/zjjcJasdaKZ)"
        )
        self.assertListEqual(
            [
                ("link", "https://i.imgur.com/zjjcJKZ"),
                ("linky", "https://i.imgur.com/zjjcJasdaKZ"),
            ],
            matches,
        )


class TestSplitLinksImages(unittest.TestCase):
    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ) and another [second image](https://i.imgur.com/3elNhQu)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.LINK, "https://i.imgur.com/zjjcJKZ"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.LINK, "https://i.imgur.com/3elNhQu"),
            ],
            new_nodes,
        )


class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_text_nodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(nodes, expected_nodes)


if __name__ == "__main__":
    unittest.main()

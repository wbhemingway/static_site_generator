from htmlnode import LeafNode
from textnode import TextNode, TextType


def text_node_to_html_node(text_node: TextNode):
    if text_node.type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    tag = None
    props = None
    text = text_node.text
    if text_node.type == TextType.BOLD:
        tag = "b"
    elif text_node.type == TextType.ITALIC:
        tag = "i"
    elif text_node.type == TextType.CODE:
        tag = "code"
    elif text_node.type == TextType.LINK:
        tag = "a"
        props = {"href": text_node.url}
    elif text_node.type == TextType.IMAGE:
        tag = "img"
        text = ""
        props = {
            "src": text_node.url,
            "alt": text_node.text,
        }

    return LeafNode(tag, text, props)

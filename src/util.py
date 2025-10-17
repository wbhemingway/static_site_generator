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


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        delim_count = node.text.count(delimiter)
        if delim_count % 2 != 0:
            raise Exception(f"No closing delimiter found for {delimiter}")

        new_strs = node.text.split(delimiter)

        for i, split in enumerate(new_strs):
            if i % 2 == 0 and split != "":
                new_nodes.append(TextNode(split, node.type))
            elif i % 2 == 1:
                new_nodes.append(TextNode(split, text_type))

    return new_nodes

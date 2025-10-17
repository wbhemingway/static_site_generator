import re

from htmlnode import LeafNode
from textnode import TextNode, TextType


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
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
        if node.type != TextType.TEXT:
            new_nodes.append(node)
            continue
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


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    nodes = [node]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    delims = {
        "**": TextType.BOLD,
        "`": TextType.CODE,
        "_": TextType.ITALIC,
    }

    for delim, t in delims.items():
        nodes = split_nodes_delimiter(nodes, delim, t)

    return nodes

from enum import Enum
from typing import Optional


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text: str, type: TextType, url: Optional[str] = None):
        self.text = text
        self.type = TextType(type)
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.type == other.type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.type.value}, {self.url})"

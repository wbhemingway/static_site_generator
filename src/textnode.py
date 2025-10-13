from enum import Enum

class TextType(Enum):
    BOLD_TEXT = "bold"
    ITALIC_TEXT = "italic"
    CODE_TEXT = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, type, url = None):
        self.text = text
        self.type = TextType(type)
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.type == other.type and self.url == other.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.type.value}, {self.url})"
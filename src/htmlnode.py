
class HtmlNode:
    def __init__(self, tag: str | None=None, value: str | None=None, children: list["HtmlNode"] | None=None, props: dict | None=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> Exception:
        raise NotImplementedError

    def props_to_html(self) -> str:
        if not self.props:
            return ""
        prop_list = []
        for k, v in self.props.items():
            prop_list.append(f'{k}="{v}"')
        if not prop_list:
            return ""
        return " " + " ".join(prop_list)

    def __repr__(self):
        return f"HtmlNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HtmlNode):
    def __init__(self, tag: str, value: str, props: list[str] | None=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError

        if self.tag is None:
            return self.value

        props = self.props_to_html()
        return f"<{self.tag}{props}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HtmlNode):
    def __init__(self, tag: str, children: list[HtmlNode], props: list[str] | None=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError
        if self.children is None:
            raise ValueError("No children")

        inner = []
        for child in self.children:
            inner.append(child.to_html())

        inner_text = "".join(inner)

        return f"<{self.tag}>{inner_text}</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"

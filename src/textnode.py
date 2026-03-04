from enum import Enum
from leafnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

    @classmethod
    def is_valid(cls, value:str) -> bool:
        try:
            cls(value)
            return True
        except ValueError:
            return False

class TextNode:
    def __init__(self, text, text_type, url=None):
        """
        Constructor

        text(string): Text content
        text_type(TextType): Type of node
        url(string): Url
        """

        if text is None:
            raise ValueError("TextNode text cannot be None")
        if text_type is None:
            raise ValueError("TextNode text_type cannot be None")

        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, anode):
        """Equality tester with another node"""
        if self.text != anode.text:
            return False
        if self.text_type != anode.text_type:
            return False
        if self.url != anode.url:
            return False
        return True

    def __repr__(self):
        """
        Simple print with value from the enum above
        """
        return f'TextNode("{self.text}", {self.text_type.value}, {self.url})'


def text_node_to_html_node(text_node: TextNode):
    if text_node.text_type not in TextType:
        raise ValueError("TextNode.text_type not in TextType enum.")
    
    tag_map = {
        TextType.TEXT: None,
        TextType.BOLD: "b",
        TextType.ITALIC: "i",
        TextType.CODE: "code",
        TextType.LINK: "a",
        TextType.IMAGE: "img",
    }
    tag = tag_map[text_node.text_type]

    if text_node.text_type == TextType.LINK:
        prop = {"href": text_node.url}
        value = text_node.text
    elif text_node.text_type == TextType.IMAGE:
        prop = {
            "src": text_node.url, 
            "alt": text_node.text
        }
        value = ""
    else:
        prop = None
        value = text_node.text

    return LeafNode(tag=tag,
                    value=value,
                    props=prop
                    )


if __name__ == "__main__":
    mynode = TextNode("some text", TextType.TEXT, "some url")
    print(mynode)
    
    print('-----------------html conversion----------')
    node = TextNode("This is a text node", TextType.TEXT)
    html_node = text_node_to_html_node(node)
    print(html_node.to_html())
    
    bold_node = TextNode("This is a bold node", TextType.BOLD)
    bold_html_node = text_node_to_html_node(bold_node)
    print(bold_html_node.to_html())

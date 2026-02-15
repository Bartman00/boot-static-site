from enum import Enum


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


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
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


if __name__ == "__main__":
    mynode = TextNode("some text", TextType.TEXT, "some url")
    print(mynode)

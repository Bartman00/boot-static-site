from htmlnode import HTMLNode
from leafnode import LeafNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children: list[HTMLNode], props=None):
        assert tag is not None, "ParentNodede needs to have a tag"
        assert children is not None, "ParentNode needs to have children"
        assert len(children) > 0, "ParentNode needs at least one child"
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.children is None:
            raise ValueError("ParentNode needs to have children")
        if self.tag is None:
            raise ValueError("ParentNode needs to have a tag")

        ret = f"<{self.tag}"
        if self.props is not None:
            ret += self.props_to_html()
        ret += ">"

        for child in self.children:
            ret += child.to_html()

        ret += f"</{self.tag}>"

        return ret


if __name__ == "__main__":
    print("inside Parent Node")

    node = ParentNode(
        "<p>",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],
    )
    print(node.to_html())
    print('-------------------------------')
    print(node)
    print('------------------------------')

from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):

        assert value is not None, "LeafNode value can't be None"
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("leaf nodes require a value")

        if self.tag is None:
            return self.value

        ret = f"<{self.tag}"
        if self.props is not None:
            ret += " " + self.props_to_html()
        ret += ">"

        ret += self.value
        ret += f"</{self.tag}>"

        return ret

    def __repr__(self):

        ret = f"tag = {self.tag}"
        ret += f"\nvalue = {self.value}"

        if self.props is None:
            ret += "\nprops = None"
        else:
            ret += "\n\nprops:\n"
            for k, v in self.props.items():
                ret += f"{k}: {v}\n"

        return ret


if __name__ == "__main__":
    print("Inside leafnode.py")
    leaf = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
    print(leaf.to_html())

    print(leaf)

    leaf_2 = LeafNode("p", "This is a paragraph")
    print(leaf_2.to_html())
    
    print(f"Is LeafNode an HTMLNode?: {isinstance(leaf, HTMLNode)}")

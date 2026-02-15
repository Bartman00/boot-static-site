class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        """
        Constructor

        tag(string) = Tag name p, a, h1, etc.
        value(string) = Value inside the HTML tab
        children(list) = HTMLNodes objects for tags inside this node
        props(dict) = Attibutes such as href

        returns(None)
        """

        assert tag is None or isinstance(tag, str), (
            "HTMLNode tag needs to be None or a string"
        )
        assert value is None or isinstance(value, str), (
            "HTMLNode tag needs to be None or a string"
        )
        if children is not None:
            assert isinstance(children, list), (
                "HTMLNode children needs to be None or a list"
            )
            assert all(isinstance(child, str) for child in children), (
                "HTMLNode children all need to be strings"
            )
        assert props is None or isinstance(props, dict), \
            "HTMLNode props needs to be None or a dictionary"
        assert value is not None or children is not None, \
            "HTMLNode needs either value or children to not be none"

        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError(
            "to_html should not be called on the HTMLNode. Only by children"
        )

    def props_to_html(self):
        ret = ""
        if self.props is None:
            return ret
        
        # Included leading space per problem instructions
        for k, v in self.props.items():
            ret += f' {k}="{v}"'
        
        return ret

    def __repr__(self):
        ret = f"tag = {self.tag}"
        ret += f"\nvalue = {self.value}"

        if self.children is None:
            ret += "\nchildren = None"
        else:
            ret += "\nchildren:\n"
            ret += "\n".join(self.children)

        if self.props is None:
            ret += "\nprops = None"
        else:
            ret += "\nprops:\n"
            ret += "\n".join(self.props)

        return ret



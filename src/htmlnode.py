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
            "HTMLNode value needs to be None or a string"
        )
        if children is not None:
            assert isinstance(children, list), (
                "HTMLNode children needs to be None or a list"
            )
            assert all(isinstance(child, HTMLNode) for child in children), (
                "HTMLNode children all need to be HTMLNodes"
            )
        assert props is None or isinstance(props, dict), \
            "HTMLNode props needs to be None or a dictionary"
        assert value is not None or children is not None, \
            "HTMLNode needs either value or children to not be none"

        # Remove "<" and ">" marks if included
        if tag is None or tag[0] != "<":
            self.tag = tag
        elif tag[0] == "<":
            if tag[-1] == ">":
                self.tag = tag[1:-1]
            else:
                raise ValueError("If tag starts with '<', it needs to end with '>'")
        
        # Other values are copied in
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
        
        return ret.strip()

    def __repr__(self):
        ret = f"tag = {self.tag}"
        ret += f"\nvalue = {self.value}"

        if self.children is None:
            ret += "\nchildren = None"
        else:
            ret += "\nchildren:\n"
            for i, child in enumerate(self.children):
                ret += f"------- Child {i} -------"
                ret += f"\n {child}\n"
            ret += "------- End Children -------"

        if self.props is None:
            ret += "\nparent props = None"
        else:
            ret += "\nparent props:\n"
            ret += "\n".join(self.props)

        return ret

    def __eq__(self, other):
        
        if self.tag != other.tag:
            return False

        if self.value != other.value:
            return False
        
        if type(self.children) is not type(other.children):
            return False

        if type(self.children) is list:
            if len(self.children) != len(other.children):
                return False
            
            for child, other_child in zip(self.children, other.children):
                if child != other_child:
                    return False

        if type(self.props) is not type(other.props):
            return False
            
        if type(self.props) is dict:
            
            # print("Checking dictionary")
            for k, v in self.props.items():
                # print(f"{k=} = {v=}")
                # print(f"other[{k}].get = {other.props.get(k)}")
                if other.props.get(k) != v:
                    return False
                    
            for k, v in other.props.items():
                if self.props.get(k) != v:
                    return False

        return True




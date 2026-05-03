from htmlnode import HTMLNode

def markdown_to_html_node(md):
    """
    Driver of converting markdown into a single parent HTML Node
    that one parent contains many children HTMLNode Ojects
    
    boot.dev instructions:
    1. Split the markdown into blocks
    2. Loop over each block:
        2.1 Determine type of block
        2.2 Based on type, create new HTMLNode
        2.3 Assign proper child HTMLNode to the block node
        2.4 `Code` block is special. Shoud NOT do any inline markdown
    3. Make all block nodes children under a single parent HTML Node
    should be a div. Return it
    4. Create unit tests.
    """

    trunk = HTMLNode(tag="<div>", value="")

    return trunk

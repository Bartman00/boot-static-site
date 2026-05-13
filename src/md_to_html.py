from block import BlockType, block_to_block_type, markdown_to_blocks
from parentnode import ParentNode
from leafnode import LeafNode
from parse import combined_split
from textnode import text_node_to_html_node


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

    Each paragraph block is a single HTMLNode and even if there are
    multiple lines, they are rendered as a single paragraph. New lines
    are converted to spaces

    so:
    This is **bolded** paragraph
    text in a p
    tag here

    becomes:
    <div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>
    """

    # trunk = ParentNode(tag="<div>", children=[])

    blocks = markdown_to_blocks(md)
    children = []

    for block in blocks:
        children.append(create_block_html_node(block))

    trunk = ParentNode(tag="<div>", children=children)
    return trunk


def create_block_html_node(block):
    # Determine block type and return using appropriate helper

    if len(block) < 1:
        return None
    block_type = block_to_block_type(block)
    # print(f"{block_type=}")

    if block_type == BlockType.PARAGRAPH:
        return create_paragraph_block(block)

    elif block_type == BlockType.HEADING:
        return create_heading_block(block)

    elif block_type == BlockType.CODE:
        # Don't pass into text node conversion
        return create_code_block(block)

    elif block_type == BlockType.QUOTE:
        return create_quote_block(block)

    elif block_type == BlockType.UNORDERED_LIST:
        return create_unordered_block(block)

    elif block_type == BlockType.ORDERED_LIST:
        return create_ordered_block(block)

    raise ValueError("create_block_html_node could not find a block")


def create_paragraph_block(block):
    # Generate the paragraph block

    # substitute any new lines for spaces
    block.replace("\n", " ")

    # Replace any multiple lines with a single line
    block = " ".join(block.split())

    leaf_nodes = create_line_leaves(block)
    parent_node = ParentNode(tag="p", children=leaf_nodes)
    return parent_node

    abcd
    abcd
    abcd

def create_unordered_block(block):
    # Generate an unordered list block

    lines = block.split("\n")
    lines = [line.strip() for line in lines]
    lines = [line for line in lines if len(line) > 0]
    # print("Lines: ")
    # print(lines)
    line_nodes = []

    for line in lines:
        # print(line)
        line = line[2:]
        leaves = create_line_leaves(line)

        if len(leaves) == 1:
            # Only one leave. Create a single leaf
            list_parent = ParentNode(tag="li", children=[leaves[0]])
            line_nodes.append(list_parent)
        elif len(leaves) > 1:
            list_parent = ParentNode(tag="li", children=leaves)
            line_nodes.append(list_parent)
        else:
            raise ValueError("Somehow, don't have any leaves in create_unordered_block")

    parent_node = ParentNode(tag="ul", children=line_nodes)
    return parent_node


def create_ordered_block(block):
    # Generate an ordered list block

    lines = block.split("\n")
    lines = [line.strip() for line in lines]
    lines = [line for line in lines if len(line) > 0]
    # print("Lines: ")
    # print(lines)
    line_nodes = []

    for line in lines:
        # print(line)
        line = line.split(" ", 1)[1]
        leaves = create_line_leaves(line)

        if len(leaves) == 1:
            # Only one leave. Create a single leaf
            list_parent = ParentNode(tag="li", children=[leaves[0]])
            line_nodes.append(list_parent)
        elif len(leaves) > 1:
            list_parent = ParentNode(tag="li", children=leaves)
            line_nodes.append(list_parent)
        else:
            raise ValueError("Somehow, don't have any leaves in create_unordered_block")

    parent_node = ParentNode(tag="ol", children=line_nodes)
    return parent_node


def create_heading_block(block):
    # Generate the heading block

    split_text = block.split(" ", 1)

    heading_level = len(split_text[0])
    line_text = split_text[1]

    leaf_nodes = create_line_leaves(line_text)
    parent_node = ParentNode(tag=f"h{heading_level}", children=leaf_nodes)
    return parent_node


def create_quote_block(block):

    lines = block.split("\n")
    lines = [line.strip() for line in lines]
    lines = [line for line in lines if len(line) > 0]
    lines = [line[2:] for line in lines]  # remove "< "

    recombined = "\n".join(lines)
    leaves = create_line_leaves(recombined)

    parent_node = ParentNode(tag="blockquote", children=leaves)
    return parent_node


def create_line_leaves(line):

    # if "\n" in line:
    #     raise ValueError("create_line_leaves should be only one line")

    text_nodes = combined_split(line)
    # print("\ntext_nodes")
    # for node in text_nodes:
    #     print(node)
    leaf_nodes = [text_node_to_html_node(node) for node in text_nodes]
    # print("\nleaf_nodes")
    # for node in leaf_nodes:
    #     print("--- New Leaf---")
    #     print(node)
    return leaf_nodes

def create_code_block(block):
    # Doesn't perform inline changes unlike the others
    lines = block.split("\n")
    lines = lines[1:-1]
    # lines = [line.strip() for line in lines]
    lines = [line for line in lines if len(line) > 0]
    reformed = "\n".join(lines)
    reformed = reformed + "\n"
    
    # print(reformed)
    leaf = LeafNode(tag="code", value=reformed)
    return ParentNode(tag="pre", children=[leaf])

if __name__ == "__main__":
    md = """
    A simple paragraph
    with multiple lines
    """

    result = create_paragraph_block(md).to_html()
    print("\nResult:")
    print(result)

    # expected_leafs = [LeafNode(tag=None,
    #                           value = "A simple paragraph")]
    # expected = ParentNode(tag="p", children=expected_leafs)
    print("------ Bold test ------")
    md = "Text with some **bold** in it"
    result = create_paragraph_block(md)

    print("-------- Empty Test  ------")
    md = ""
    result = create_block_html_node(md)
    print(result)

    print("\n-------- Unordered Test  ------")
    block = """
- Item 1
- Item 2
- Item 3

- Item 4
- Item 5
- Item 6
"""
    """
    result = markdown_to_html_node(block)
    print(result.to_html())
    expected = "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul><ul><li>Item 4</li><li>Item 5</li><li>Item 6</li></ul></div>"
    print(result.to_html() == expected)
    """
    print("\n-------- Ordered Test  ------")
    md = """
1. Numbered 1
2. Numbered 2
3. Numbered 3
"""
    result = markdown_to_html_node(md).to_html()
    print(result)

    print("\n-------- Heading test  ------")
    md = """###### Heading 1

## Heading 2 **bolded**
"""
    result = markdown_to_html_node(md).to_html()
    print(result)

    print("\n-------- Blockquote test ------")
    md = """> Blockquote 1 **bold**
"""
    result = markdown_to_html_node(md).to_html()
    print(result)

from htmlnode import HTMLNode
from block import markdown_to_blocks, block_to_block_type, BlockType
from parentnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from parse import combined_split
from leafnode import LeafNode

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
    <p>This is <b>bolded</b> paragraph text in a p tag here</p>
    """

    trunk = ParentNode(tag="<div>", children=[])
    
    blocks = markdown_to_blocks(md)
    
    if len(blocks) == 1:
        return None
    
    for block in blocks:
        trunk.children.append(create_block_html_node(block))
            

    return trunk

def create_block_html_node(block):

    block_type = block_to_block_type(block)

    if block_type == BlockType.PARAGRAPH:
        return create_paragraph_block(block)

    elif block_type == BlockType.HEADING:
        pass
        
    elif block_type == BlockType.CODE:
        # Don't pass into text node conversion
        pass
        
    elif block_type == BlockType.QUOTE:
        pass
    
    elif block_type == BlockType.UNORDERED_LIST:
        pass

    elif block_type == BlockType.ORDERED_LIST:
        pass

    raise ValueError("create_block_html_node could not find a block")
    
def create_paragraph_block(block):
    # Generate the paragraph block
    
    if len(block) < 1:
        return None
    
    # substitute any new lines for spaces
    block.replace("\n", " ")

    # Replace any multiple lines with a single line
    block = " ".join(block.split())
    
    leaf_nodes = create_line_leaves(block)
    parent_node = ParentNode(tag="p", children=leaf_nodes)
    return parent_node
    
def create_line_leaves(line):
    
    if "\n" in line:
        raise ValueError("create_line_leaves should be only one line")

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
    
if __name__ == "__main__":

    md = """
    A simple paragraph
    with multiple lines
    """

    result = create_paragraph_block(md)
    print("\nResult:")
    print(result)
    
    # expected_leafs = [LeafNode(tag=None,
    #                           value = "A simple paragraph")]
    # expected = ParentNode(tag="p", children=expected_leafs)
    print('------ Bold test ------')
    md = "Text with some **bold** in it"
    result = create_paragraph_block(md)
    
    print('-------- Empty Test  ------')
    md = ""
    result = create_paragraph_block(md)
    print(result)

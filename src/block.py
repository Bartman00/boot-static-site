from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    # Returns the BlockType enum
    # Block is a single string that can include multiple lines
    
    
    if not isinstance(block, str):
        raise ValueError("block_to_block_type needs a string input")
    if len(block) < 1:
        raise ValueError("block_to_block_type can't have an empty string")
    if "\n\n" in block:
        raise ValueError("block_to_block_type can't have double blank lines")
        
    lines = block.split("\n")
        
    if len(lines) < 1:
        raise ValueError("Block needs at least one line")

    # Check the first character to see if it fits any of these
    # and avoid longer test
    start_characters = "#`>-123456789"
    # print(block[0][0])
    if lines[0][0] not in start_characters:
        # print("missing first char")
        return BlockType.PARAGRAPH

    # Heading starts with 1-6 # then a space
    # print("heading regex:")
    # print(re.findall(r"#{1,6}\s.*", lines[0]))
    # print(f"{lines[0]=}")
    if len(re.findall(r"^#{1,6}\s.*", lines[0])) > 0:
        return BlockType.HEADING
    
    # Code starts with ``` then a new line and ends with ```
    if (len(lines) >= 2 and 
          lines[0][:3] == "```" and 
          lines[-1][-3:] == "```"):
        return BlockType.CODE
    
    # Quotes every line starts with >
    if len([line for line in lines if line[0] == ">"]) == len(lines):
        # print(block[0][0])
        return BlockType.QUOTE
    
    # Unordered lists all start with - then a space
    if len([line for line in lines if line[:2] == "- "]) == len(lines):
        return BlockType.UNORDERED_LIST
    
    # Ordered lists all start with 1. and need to go up every line
    is_ordered_list = True
    digit = "1"
    for line in lines:
        if line[0:len(digit)+2] != digit+". ":
            is_ordered_list = False
            break
        digit = str(int(digit)+1)

    if is_ordered_list:
        return BlockType.ORDERED_LIST
            
    # Default
    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown):

    if len(markdown) < 1:
        return []

    ret = markdown.split("\n\n")
    ret = [b.strip() for b in ret]
    ret = [b for b in ret if len(b) > 0]
    return ret


if __name__ == "__main__":
    print("inside block.py")

    md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
    blocks = markdown_to_blocks(md)

    for block in blocks:
        print("\n")
        print(block)

    print("\n")
    print(f"len(blocks)={len(blocks)}")

    print("\n\n----------BLOCK TO BLOCK TYPE-----------")
    
    md = """
> Quote 1
> Quote 2
"""
    blocks = markdown_to_blocks(md)
    print("blocks:")
    print(f"len:{len(blocks)}")
    for block in blocks:
        print(block)
        print(block_to_block_type(block))
        print("\n")


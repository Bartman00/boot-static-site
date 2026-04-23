
def markdown_to_blocks(markdown):

    if len(markdown) < 1:
        return []

    ret = markdown.split('\n\n')
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

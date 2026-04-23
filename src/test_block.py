import unittest
from block import markdown_to_blocks

class TestTextNode(unittest.TestCase):
        
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_blocks_empty(self):
        md = """
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,[]
        )
        
    def test_stripping(self):
        md = """
Some text with spaces at the end     

And another block\n\n    Block with spaces at the beginning
"""
        blocks = markdown_to_blocks(md)
        
        self.assertEqual(
                blocks,[
                    "Some text with spaces at the end",
                    "And another block",
                    "Block with spaces at the beginning"
                    ]
                )

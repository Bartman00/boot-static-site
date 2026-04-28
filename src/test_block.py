import unittest
from block import markdown_to_blocks, block_to_block_type, BlockType

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
    
    def test_paragraph(self):
        md = "Paragraph 01"
        blocks = markdown_to_blocks(md)
        result = []
        for block in blocks:
            result.append(block_to_block_type(block))
        expected = [BlockType.PARAGRAPH]
        self.assertEqual(result, expected)
        
        md = """
Some text with spaces at the end     

And another block\n\n    Block with spaces at the beginning
"""
        blocks = markdown_to_blocks(md)
        result = []
        for block in blocks:
            result.append(block_to_block_type(block))
        expected = [BlockType.PARAGRAPH,
                    BlockType.PARAGRAPH,
                    BlockType.PARAGRAPH]
        self.assertEqual(result, expected)
        
        md = "1 Not a numbered list"
        result = [block_to_block_type(block) for block in markdown_to_blocks(md)]
        expected = [BlockType.PARAGRAPH]
        self.assertEqual(result, expected)
        
        md = "```Not code if doesn't end right``"
        result = [block_to_block_type(block) for block in markdown_to_blocks(md)]
        expected = [BlockType.PARAGRAPH]
        self.assertEqual(result, expected)
        

        md = "1.Numbered lists need spaces"
        result = [block_to_block_type(block) for block in markdown_to_blocks(md)]
        expected = [BlockType.PARAGRAPH]
        self.assertEqual(result, expected)
        
        md = "1 Numbered lists need periods"
        result = [block_to_block_type(block) for block in markdown_to_blocks(md)]
        expected = [BlockType.PARAGRAPH]
        self.assertEqual(result, expected)
        
        md = """
> This would be a quotes block
but every line needs >
        """
        result = [block_to_block_type(block) for block in markdown_to_blocks(md)]
        expected = [BlockType.PARAGRAPH]
        self.assertEqual(result, expected)
        
        md = """
- Should only count as an unordered list
-If all lines conform
"""
        result = [block_to_block_type(block) for block in markdown_to_blocks(md)]
        expected = [BlockType.PARAGRAPH]
        self.assertEqual(result, expected)
        
        
    def test_block_type_error(self):

        # Check that some are errors
        md = """Paragraph 01


        Paragraph 02
        """
        with self.assertRaises(ValueError):
            # Should be split before being passed
            print(block_to_block_type(md))
            
            
        with self.assertRaises(ValueError):
            # Need to pass strings
            print(block_to_block_type(2))
            
        with self.assertRaises(ValueError):
            # Cannot pass empty strings
            print(block_to_block_type(""))
        
        bad_blocks = ["first ok", 1]

        with self.assertRaises(ValueError):
            # Cannot pass a list
            print(block_to_block_type(bad_blocks))
            
        with self.assertRaises(ValueError):
            # Cannot pass a list
            print(block_to_block_type([]))
    
    def test_headings(self):

        md = "# Heading 1"
        result = [block_to_block_type(block) for block in markdown_to_blocks(md)]
        expected = [BlockType.HEADING]
        self.assertEqual(result, expected)
        
        md = """
# Heading 1

## Heading 2

### Heading 3

#### Heading 4

##### Heading 5

###### Heading 6

####### Not a heading
"""
        
        result = [block_to_block_type(block) for block in markdown_to_blocks(md)]
        expected = [BlockType.HEADING,
                    BlockType.HEADING,
                    BlockType.HEADING,
                    BlockType.HEADING,
                    BlockType.HEADING,
                    BlockType.HEADING,
                    BlockType.PARAGRAPH,
                    ]
        self.assertEqual(result, expected)
        
        md = """
# Heading
I think everything is a heading if the first line is.
"""
        
        result = [block_to_block_type(block) for block in markdown_to_blocks(md)]
        expected = [BlockType.HEADING]
        self.assertEqual(result, expected)
        
    def test_code_block(self):
        
        md = """
        ```
        Some code
        ```
        """
        result = [block_to_block_type(block) for block in markdown_to_blocks(md)]
        expected = [BlockType.CODE]
        self.assertEqual(result, expected)
        
        md = """
        ```
        Still code```
        """
        result = [block_to_block_type(block) for block in markdown_to_blocks(md)]
        expected = [BlockType.CODE]
        self.assertEqual(result, expected)
        
        md = """
        ```
        Still code
        And then
        some more code
        Should ignore
        ```
        
        """
        result = [block_to_block_type(block) for block in markdown_to_blocks(md)]
        expected = [BlockType.CODE]
        self.assertEqual(result, expected)
        
        md = """
        ```
        Still code
        > Should still call
        1. All of this code
        - Always```
        """
        result = [block_to_block_type(block) for block in markdown_to_blocks(md)]
        expected = [BlockType.CODE]
        self.assertEqual(result, expected)
        
    def test_quotes(self):

        md = """
        > Quote block
        """

        result = [block_to_block_type(block) for block in markdown_to_blocks(md)]
        expected = [BlockType.QUOTE]
        # self.assertEqual(result, expected)
        
        md = """
> Quote 1

> Quote 2
        """
        result = [block_to_block_type(block) for block in markdown_to_blocks(md)]
        expected = [BlockType.QUOTE, BlockType.QUOTE]
        # self.assertEqual(result, expected)

        md = """
> Quote 1
> Quote 2
        """
        result = [block_to_block_type(block) for block in markdown_to_blocks(md)]
        expected = [BlockType.QUOTE]
        self.assertEqual(result, expected)
        
        md = """
> Quote 1
> Quote 2

Paragraph
        """
        result = [block_to_block_type(block) for block in markdown_to_blocks(md)]
        expected = [BlockType.QUOTE, BlockType.PARAGRAPH]
        self.assertEqual(result, expected)
        
    def test_unordered(self):

        md = "- Simple unordered"
        result = [block_to_block_type(block) for block in markdown_to_blocks(md)]
        expected = [BlockType.UNORDERED_LIST]
        self.assertEqual(result, expected)
        
        md = "- Two\n\n- Unordered"
        result = [block_to_block_type(block) for block in markdown_to_blocks(md)]
        expected = [BlockType.UNORDERED_LIST, BlockType.UNORDERED_LIST]
        self.assertEqual(result, expected)
        
        md = "- Two\n- Unordered"
        result = [block_to_block_type(block) for block in markdown_to_blocks(md)]
        expected = [BlockType.UNORDERED_LIST]
        self.assertEqual(result, expected)
        
        md = "- Two\n\n- Unordered\n\n-paragraph"
        result = [block_to_block_type(block) for block in markdown_to_blocks(md)]
        expected = [BlockType.UNORDERED_LIST, BlockType.UNORDERED_LIST, BlockType.PARAGRAPH]
        self.assertEqual(result, expected)
        
    
    def test_ordered(self):

        md = "1. Simple ordered"
        result = [block_to_block_type(block) for block in markdown_to_blocks(md)]
        expected = [BlockType.ORDERED_LIST]
        self.assertEqual(result, expected)
        
        md = "1. Two\n\n2. Unordered"
        result = [block_to_block_type(block) for block in markdown_to_blocks(md)]
        expected = [BlockType.ORDERED_LIST, BlockType.PARAGRAPH]
        self.assertEqual(result, expected)
        
        md = "1. Two\n2. Unordered"
        result = [block_to_block_type(block) for block in markdown_to_blocks(md)]
        expected = [BlockType.ORDERED_LIST]
        self.assertEqual(result, expected)
        
        md = "1. Two\n\n2. Unordered\n\n1. paragraph"
        result = [block_to_block_type(block) for block in markdown_to_blocks(md)]
        expected = [BlockType.ORDERED_LIST, BlockType.PARAGRAPH, BlockType.ORDERED_LIST]
        self.assertEqual(result, expected)

    def test_combined(self):

        
        md = """
This is a paragraph block

# This is a heading

1. Numbered list

> Quote block

- Unordered list

```
Code block```
"""
    
        result = [block_to_block_type(block) for block in markdown_to_blocks(md)]
        expected = [BlockType.PARAGRAPH,
                    BlockType.HEADING,
                    BlockType.ORDERED_LIST,
                    BlockType.QUOTE,
                    BlockType.UNORDERED_LIST,
                    BlockType.CODE]
        self.assertEqual(result, expected)
        
        md = """
```
First code block
```

```
Second code block
```

1. First
2. Second
3. Third

###### Maximum heading!

> Bigger
> Quote

- Unorder
- will
- Reign

1. This
> Is
- Actually a paragraph

Another paragraph

```
third code
block
```

# Final heading
"""


        result = [block_to_block_type(block) for block in markdown_to_blocks(md)]
        expected = [BlockType.CODE,
                    BlockType.CODE,
                    BlockType.ORDERED_LIST,
                    BlockType.HEADING,
                    BlockType.QUOTE,
                    BlockType.UNORDERED_LIST,
                    BlockType.PARAGRAPH,
                    BlockType.PARAGRAPH,
                    BlockType.CODE,
                    BlockType.HEADING,
                    ]
        self.assertEqual(result, expected)


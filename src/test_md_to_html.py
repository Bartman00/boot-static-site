import unittest

from leafnode import LeafNode
from md_to_html import (
    create_block_html_node,
    create_line_leaves,
    create_paragraph_block,
    markdown_to_html_node,
)
from parentnode import ParentNode


class TestMDtoHTML(unittest.TestCase):
    def test_basic(self):
        block = """
        A simple paragraph
        with multiple
        lines
        """
        result = markdown_to_html_node(block).to_html()
        expected = "<div><p>A simple paragraph with multiple lines</p></div>"
        self.assertEqual(result, expected)

    def test_paragraphs(self):
        # From boot.dev
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    # ------ Paragraph -------
    def test_create_paragraph_block(self):

        block = """
        A simple paragraph
        with multiple
        lines
        """
        result = create_paragraph_block(block)
        expected_leafs = [
            LeafNode(tag=None, value="A simple paragraph with multiple lines")
        ]
        expected = ParentNode(tag="p", children=expected_leafs)
        self.assertEqual(result, expected)

        html = result.to_html()
        self.assertEqual(html, "<p>A simple paragraph with multiple lines</p>")

    def test_empty_paragraph(self):
        md = ""
        result = create_block_html_node(md)
        expected = None
        self.assertEqual(result, expected)

    def test_bold_paragraph(self):
        block = "Text with some **bold** in it"
        result = create_paragraph_block(block)
        expected_leafs = [
            LeafNode(tag=None, value="Text with some "),
            LeafNode(tag="b", value="bold"),
            LeafNode(tag=None, value=" in it"),
        ]
        expected = ParentNode(tag="p", children=expected_leafs)
        self.assertEqual(result, expected)

        html = result.to_html()
        expected_html = "<p>Text with some <b>bold</b> in it</p>"
        self.assertEqual(html, expected_html)

    def test_mixed_paragraph(self):
        block = "Text with _some_ **bold** in `it`"
        result = create_paragraph_block(block)
        expected_leafs = [
            LeafNode(tag=None, value="Text with "),
            LeafNode(tag="i", value="some"),
            LeafNode(tag=None, value=" "),
            LeafNode(tag="b", value="bold"),
            LeafNode(tag=None, value=" in "),
            LeafNode(tag="code", value="it"),
        ]
        expected = ParentNode(tag="p", children=expected_leafs)
        self.assertEqual(result, expected)

        html = result.to_html()
        expected_html = "<p>Text with <i>some</i> <b>bold</b> in <code>it</code></p>"
        self.assertEqual(html, expected_html)

    def test_link_paragraph(self):
        block = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif)"
        result = create_paragraph_block(block)
        expected_leafs = [
            LeafNode(tag=None, value="This is text with a "),
            LeafNode(
                tag="a",
                value="rick roll",
                props={"href": "https://i.imgur.com/aKaOqIh.gif"},
            ),
        ]
        expected = ParentNode(tag="p", children=expected_leafs)
        self.assertEqual(result, expected)

        html = result.to_html()
        expected_html = '<p>This is text with a <a href="https://i.imgur.com/aKaOqIh.gif">rick roll</a></p>'
        self.assertEqual(html, expected_html)

    def test_image_paragraph(self):
        block = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        result = create_paragraph_block(block)
        expected_leafs = [
            LeafNode(tag=None, value="This is text with a "),
            LeafNode(
                tag="img",
                value="",
                props={"src": "https://i.imgur.com/aKaOqIh.gif", "alt": "rick roll"},
            ),
        ]
        expected = ParentNode(tag="p", children=expected_leafs)
        self.assertEqual(result, expected)

        html = result.to_html()
        expected_html = '<p>This is text with a <img src="https://i.imgur.com/aKaOqIh.gif" alt="rick roll"></img></p>'
        self.assertEqual(html, expected_html)

    def test_create_line_leaves(self):

        block = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        result = create_line_leaves(block)
        expected_leafs = [
            LeafNode(tag=None, value="This is text with a "),
            LeafNode(
                tag="img",
                value="",
                props={"src": "https://i.imgur.com/aKaOqIh.gif", "alt": "rick roll"},
            ),
        ]
        self.assertEqual(result, expected_leafs)

    def test_create_unordered_block(self):
        block = """
- Item 1
- Item 2
- Item 3
"""
        result = create_block_html_node(block).to_html()
        expected = "<ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul>"
        self.assertEqual(result, expected)

    def test_create_unordered_block_2(self):
        block = """
- Item 1
- Item 2
- Item 3

- Item 4
- Item 5
- Item 6
"""
        result = markdown_to_html_node(block).to_html()
        expected = "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul><ul><li>Item 4</li><li>Item 5</li><li>Item 6</li></ul></div>"
        self.assertEqual(result, expected)
    
    def test_create_mixed_lists(self):
        block = """
- Item 1
- Item 2
- Item 3

1. Numbered 4
2. Numbered 5
3. Numbered 6
"""
        result = markdown_to_html_node(block).to_html()
        expected = "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul><ol><li>Numbered 4</li><li>Numbered 5</li><li>Numbered 6</li></ol></div>"
        self.assertEqual(result, expected)
        
    def test_headings(self):

        md = """###### Heading 1

## Heading 2 **bolded**
"""
        result = markdown_to_html_node(md).to_html()
        expected = "<div><h6>Heading 1</h6><h2>Heading 2 <b>bolded</b></h2></div>"
        self.assertEqual(result, expected)
        
    def test_not_headings(self):
        # Misc tests for almost yeadings that should not be headings
        md = """####### Too many pounds"""
        result = markdown_to_html_node(md).to_html()
        expected = "<div><p>####### Too many pounds</p></div>"
        self.assertEqual(result, expected)
        
        md = """# Multiline
## Headings don't count"""
        result = markdown_to_html_node(md).to_html()
        expected = "<div><p># Multiline ## Headings don't count</p></div>"
        self.assertEqual(result, expected)
        
    def test_blockquote(self):

        md = """> Blockquote 1 **bold**"""
        result = markdown_to_html_node(md).to_html()
        expected = "<div><blockquote>Blockquote 1 <b>bold</b></blockquote></div>"
        self.assertEqual(result, expected)
        
        md = """> Blockquote 1
> line 2 in blockquote

> Blockquote 2
"""
        result = markdown_to_html_node(md).to_html()
        expected = "<div><blockquote>Blockquote 1\nline 2 in blockquote</blockquote><blockquote>Blockquote 2</blockquote></div>"
        self.assertEqual(result, expected)
    
    def test_codeblock(self):
        # From boot.dev
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """
    
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


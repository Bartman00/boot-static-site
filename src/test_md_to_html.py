import unittest
from md_to_html import markdown_to_html_node, create_paragraph_block
from md_to_html import create_line_leaves
from htmlnode import HTMLNode
from parentnode import ParentNode
from leafnode import LeafNode

class TestMDtoHTML(unittest.TestCase):

    def test_empty(self):
        md = ""
        # result = markdown_to_html_node(md)
        # result = markdown_to_html_node(md)
        # expected_leaves = [LeafNode(tag="p", value="")]
        # expected = ParentNode(tag="<div>", children=expected_leaves)
        # self.assertEqual(result, expected)
        
    def test_create_paragraph_block(self):

        block = """
        A simple paragraph
        with multiple
        lines
        """
        result = create_paragraph_block(block)
        expected_leafs = [LeafNode(tag=None,
                                  value = "A simple paragraph with multiple lines")]
        expected = ParentNode(tag="p", children=expected_leafs)
        self.assertEqual(result, expected)
        
        html = result.to_html()
        self.assertEqual(html,
                         "<p>A simple paragraph with multiple lines</p>"
                         )

    
    def test_empty_paragraph(self):
        md = ""
        result = create_paragraph_block(md)
        expected = None
        self.assertEqual(result, expected)
    
    def test_bold_paragraph(self):
        block = "Text with some **bold** in it"
        result = create_paragraph_block(block)
        expected_leafs = [LeafNode(tag=None, value = "Text with some "),
                          LeafNode(tag="b", value="bold"),
                          LeafNode(tag=None, value=" in it")]
        expected = ParentNode(tag="p", children=expected_leafs)
        self.assertEqual(result, expected)
        
        html = result.to_html()
        expected_html = "<p>Text with some <b>bold</b> in it</p>"
        self.assertEqual(html, expected_html)
        
    def test_mixed_paragraph(self):
        block = "Text with _some_ **bold** in `it`"
        result = create_paragraph_block(block)
        expected_leafs = [LeafNode(tag=None, value = "Text with "),
                          LeafNode(tag="i", value="some"),
                          LeafNode(tag=None, value=" "),
                          LeafNode(tag="b", value="bold"),
                          LeafNode(tag=None, value=" in "),
                          LeafNode(tag="code", value="it")]
        expected = ParentNode(tag="p", children=expected_leafs)
        self.assertEqual(result, expected)
        
        html = result.to_html()
        expected_html = "<p>Text with <i>some</i> <b>bold</b> in <code>it</code></p>"
        self.assertEqual(html, expected_html)
    
    def test_link_paragraph(self):
        block = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif)"
        result = create_paragraph_block(block)
        expected_leafs = [LeafNode(tag=None, value = "This is text with a "),
                          LeafNode(tag="a", value="rick roll", 
                                   props={'href': "https://i.imgur.com/aKaOqIh.gif"}),
                          ]
        expected = ParentNode(tag="p", children=expected_leafs)
        self.assertEqual(result, expected)
        
        html = result.to_html()
        expected_html = '<p>This is text with a <a href="https://i.imgur.com/aKaOqIh.gif">rick roll</a></p>'
        self.assertEqual(html, expected_html)
    
    def test_image_paragraph(self):
        block = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        result = create_paragraph_block(block)
        expected_leafs = [LeafNode(tag=None, value = "This is text with a "),
                          LeafNode(tag="img", value="", 
                                   props={'src': "https://i.imgur.com/aKaOqIh.gif",
                                          'alt': "rick roll"}),
                          ]
        expected = ParentNode(tag="p", children=expected_leafs)
        self.assertEqual(result, expected)
        
        html = result.to_html()
        expected_html = '<p>This is text with a <img src="https://i.imgur.com/aKaOqIh.gif" alt="rick roll"></img></p>'
        self.assertEqual(html, expected_html)
    

    def test_create_line_leaves(self):

        block = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        result = create_line_leaves(block)
        expected_leafs = [LeafNode(tag=None, value = "This is text with a "),
                          LeafNode(tag="img", value="", 
                                   props={'src': "https://i.imgur.com/aKaOqIh.gif",
                                          'alt': "rick roll"}),
                          ]
        self.assertEqual(result, expected_leafs)

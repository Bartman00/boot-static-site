import unittest
from md_to_html import markdown_to_html_node
from htmlnode import HTMLNode

class TestMDtoHTML(unittest.TestCase):

    def test_empty(self):
        md = ""
        # result = markdown_to_html_node(md)
        result = markdown_to_html_node(md)
        expected = HTMLNode(tag="<div>", value="")
        self.assertEqual(result, expected)

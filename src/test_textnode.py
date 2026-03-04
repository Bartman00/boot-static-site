import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def setUp(self) -> None:
        self.node = TextNode("This is a text node", TextType.BOLD)

    def test_eq(self):
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(self.node, node2)

    def test_neq(self):
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertNotEqual(self.node, node2)

    def test_different_url(self):
        node2 = TextNode("This is a text node", TextType.BOLD, "www.google.com")
        self.assertNotEqual(self.node, node2)

    def test_eq_url(self):
        node2 = TextNode("This is a text node", TextType.BOLD, "www.google.com")
        node3 = TextNode("This is a text node", TextType.BOLD, "www.google.com")
        self.assertEqual(node2, node3)

    def test_neq_text(self):
        node2 = TextNode("This is slightly different text", TextType.BOLD)
        self.assertNotEqual(self.node, node2)

    def test_eq_emptys(self):
        node1 = TextNode("", "")
        node2 = TextNode("", "")
        self.assertEqual(node1, node2)

    def test_eq_nourl(self):
        node2 = TextNode("This is a text node", TextType.BOLD, None)
        self.assertEqual(self.node, node2)
        
    def test_conversion(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        
    def test_text_bold_conversion(self):
        bold_node = TextNode("This is bold text", TextType.BOLD)

        bold_html = text_node_to_html_node(bold_node)
        self.assertEqual(bold_html.value, 'This is bold text')
        self.assertEqual(bold_html.tag, 'b')
        self.assertEqual(bold_html.props, None)
    
    def test_text_italic_conversion(self):
        italic_node = TextNode("This is italic text", TextType.ITALIC)
        italic_html = text_node_to_html_node(italic_node)
        self.assertEqual(italic_html.value, 'This is italic text')
        self.assertEqual(italic_html.tag, 'i')
        self.assertEqual(italic_html.props, None)
        
    def test_text_code_conversion(self):
        code_node = TextNode("This is code text", TextType.CODE) 
        code_html = text_node_to_html_node(code_node) 
        self.assertEqual(code_html.value, 'This is code text') 
        self.assertEqual(code_html.tag, 'code')
        self.assertEqual(code_html.props, None)

    def test_text_link_conversion(self):
        link_node = TextNode("This is link text", TextType.LINK, url='www.fake.com')
        link_html = text_node_to_html_node(link_node) 
        self.assertEqual(link_html.value, 'This is link text') 
        self.assertEqual(link_html.tag, 'a')
        self.assertEqual(link_html.props, {'href': 'www.fake.com'})
        
    def test_image_link_conversion(self):
        img_node = TextNode("This is image text", TextType.IMAGE, url='www.image.com')
        image_html = text_node_to_html_node(img_node)
        self.assertEqual(image_html.value, "") 
        self.assertEqual(image_html.tag, 'img')
        self.assertEqual(image_html.props['src'], 'www.image.com')
        self.assertEqual(image_html.props['alt'], 'This is image text')
        
if __name__ == "__main__":
    unittest.main()

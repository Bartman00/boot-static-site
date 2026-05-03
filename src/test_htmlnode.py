import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode

class TestTextNode(unittest.TestCase):
    def setUp(self) -> None:
        self.node = HTMLNode("<p>", "a value", 
                                [HTMLNode(value='child1'), 
                                    HTMLNode(value='child2')],
                                {'k1':'v1', 'k2':'v2'})

    def test_eq(self):

        self.assertEqual(self.node.tag, "p")
        self.assertEqual(self.node.value, "a value")
        self.assertEqual(self.node.children[0].value, "child1")
        self.assertEqual(self.node.props, {'k1':'v1', 'k2':'v2'})
        
    def test_eq_dunder(self):
        
        basic = HTMLNode("<p>", "a value")
        self.assertEqual(basic, basic)
        
        copy = HTMLNode("<p>", "a value", 
                        [HTMLNode(value='child1'), 
                            HTMLNode(value='child2')],
                        {'k1':'v1', 'k2':'v2'})
        self.assertEqual(self.node, copy)
        
        another_copy = HTMLNode("p", "a value", 
                        [HTMLNode(value='child1'), 
                            HTMLNode(value='child2')],
                        {'k1':'v1', 'k2':'v2'})
                        
        self.assertEqual(self.node, another_copy)
        
        # Changed the tag
        bad_copy = HTMLNode("d", "a value", 
                        [HTMLNode(value='child1'), 
                            HTMLNode(value='child2')],
                        {'k1':'v1', 'k2':'v2'})
        self.assertNotEqual(self.node, bad_copy)
        

        # Changed the keys
        bad_copy_2 = HTMLNode("p", "a value", 
                        [HTMLNode(value='child1'), 
                            HTMLNode(value='child2')],
                        {'key_1':'v1', 'key_2':'v2'})
        self.assertNotEqual(self.node, bad_copy_2)

    def test_assert_bad_inputs(self):

        with self.assertRaises(AssertionError):
            HTMLNode(1, 'a')
        with self.assertRaises(AssertionError):
            HTMLNode('1', 2)
        with self.assertRaises(AssertionError):
            HTMLNode('1', 'a', 'b')
        with self.assertRaises(AssertionError):
            HTMLNode(1, 'a')
        with self.assertRaises(AssertionError):
            HTMLNode('1', 'a', [1])
        with self.assertRaises(AssertionError):
            HTMLNode('1')


    def test_to_html_error(self):
        with self.assertRaises(NotImplementedError):
            self.node.to_html()

    def test_props_to_html(self):

        self.assertEqual(self.node.props_to_html(), ' k1="v1" k2="v2"')
        node2 = HTMLNode("a", "b", props={})
        self.assertEqual(node2.props_to_html(), "")


    def test_repr(self):
        text = f'{self.node}'
        # print(text)
        self.assertIn("value =", text)
        self.assertIn("children:", text)
        self.assertIn("tag =", text)
        self.assertIn("props:", text)

        min_node = HTMLNode('a', 'b')
        self.assertIn("children = None", str(min_node))
        self.assertIn("props = None", str(min_node))

    def _test_eq_emptys(self):
        node1 = TextNode("", "")
        node2 = TextNode("", "")
        self.assertEqual(node1, node2)

    def _test_eq_nourl(self):
        node2 = TextNode("This is a text node", TextType.BOLD, None)
        self.assertEqual(self.node, node2)


if __name__ == "__main__":
    unittest.main()

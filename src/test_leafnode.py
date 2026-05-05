import unittest

from leafnode import LeafNode

class TestTextNode(unittest.TestCase):
    def setUp(self) -> None:
        self.node = LeafNode("<p>", "a value", 
                             props = {'k1':'v1', 'k2':'v2'})

    def test_eq(self):

        self.assertEqual(self.node.tag, "p")
        self.assertEqual(self.node.value, "a value")
        self.assertEqual(self.node.props, {'k1':'v1', 'k2':'v2'})
        
    def test_eq_dunder(self):
        self.assertEqual(self.node, self.node)
        
        node_2 = LeafNode("<p>", "a value", 
                          props = {'k1':'v1', 'k2':'v2'})
        self.assertEqual(self.node, node_2)
        
        node_2.props['k3'] = 'v3'
        
        self.assertNotEqual(self.node, node_2)

    def test_assert_bad_inputs(self):

        with self.assertRaises(AssertionError):
            LeafNode(1, 'a')
        with self.assertRaises(AssertionError):
            LeafNode('1', 2)
        with self.assertRaises(AssertionError):
            LeafNode('1', 'a', 'b')
        with self.assertRaises(AssertionError):
            LeafNode(1, 'a')
        with self.assertRaises(AssertionError):
            LeafNode('1', 'a', [1])
        with self.assertRaises(AssertionError):
            LeafNode('1', None)
        with self.assertRaises(ValueError):
            bad_leaf = LeafNode('1', '2')
            bad_leaf.value = None
            bad_html = bad_leaf.to_html() 
            print(bad_html) # Get's the linter to shut the fuck up

    def test_props_to_html(self):

        self.assertEqual(self.node.props_to_html(), 'k1="v1" k2="v2"')
        node2 = LeafNode("a", "b", props={})
        self.assertEqual(node2.props_to_html(), "")


    def test_repr(self):
        text = f'{self.node}'
        # print(text)
        self.assertIn("value =", text)
        self.assertNotIn("children:", text)
        self.assertIn("tag =", text)
        self.assertIn("props:", text)

        min_node = LeafNode('a', 'b')
        self.assertIn("props = None", str(min_node))




if __name__ == "__main__":
    unittest.main()

import unittest

from textnode import TextNode, TextType


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


if __name__ == "__main__":
    unittest.main()

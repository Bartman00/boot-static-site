import unittest

from leafnode import LeafNode
from parentnode import ParentNode


class TestTextNode(unittest.TestCase):
    def setUp(self) -> None:
        self.base_parent = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("<i>", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

    def test_basic(self):

        self.assertEqual(self.base_parent.tag, "p")
        self.assertEqual(self.base_parent.value, None)
        self.assertEqual(self.base_parent.children[0].tag, "b")
        self.assertEqual(self.base_parent.children[1].tag, None)
        self.assertEqual(self.base_parent.children[2].tag, "i")
        self.assertEqual(self.base_parent.children[0].value, "Bold text")
        self.assertEqual(self.base_parent.children[1].value, "Normal text")
        self.assertEqual(self.base_parent.children[2].value, "italic text")
        self.assertEqual(len(self.base_parent.children), 4)

    def test_asserts(self):

        with self.assertRaises(AssertionError):
            bad_parent = ParentNode("b", [])
            print(bad_parent)  # Get linter to shut up
        with self.assertRaises(AssertionError):
            bad_parent = ParentNode("b", None)
            print(bad_parent)  # Shut up linter
        with self.assertRaises(AssertionError):
            bad_parent = ParentNode("b", ["HtmlNode"])
            print(bad_parent)
        with self.assertRaises(TypeError):
            bad_parent = ParentNode("b", LeafNode("b", "Bold Text"))
            print(bad_parent)
        with self.assertRaises(ValueError):
            bad_parent = ParentNode("b", [LeafNode("b", "Bold Text")])
            bad_parent.tag = None
            print(bad_parent.to_html())
        with self.assertRaises(ValueError):
            bad_parent = ParentNode("b", [LeafNode("b", "Bold Text")])
            bad_parent.children = None
            print(bad_parent.to_html())
        # With and without properties

    def test_grandchildren(self):
        # Tests with children of children
        parent = ParentNode(
            "p",
            [
                ParentNode(
                    "b",
                    [
                        LeafNode(None, "Normal Child Text"),
                        ParentNode("i", [LeafNode(None, "ChildText")]),
                    ],
                ),
                LeafNode(None, "Normal text"),
                LeafNode("<i>", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(parent.children[1].value, "Normal text")
        self.assertEqual(parent.children[0].children[0].value, "Normal Child Text")
        self.assertEqual(parent.children[0].children[1].children[0].value, "ChildText")

    def test_to_html(self):

        self.assertEqual(
            self.base_parent.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_grandchildren(self):

        parent = ParentNode(
            "p",
            [
                ParentNode(
                    "b",
                    [
                        LeafNode(None, "Normal Child Text"),
                        ParentNode("i", [LeafNode(None, "ChildText")]),
                    ],
                ),
                LeafNode(None, "Normal text"),
                LeafNode("<i>", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            parent.to_html(),
            "<p><b>Normal Child Text<i>ChildText</i></b>Normal text<i>italic text</i>Normal text</p>",
        )


if __name__ == "__main__":
    unittest.main()

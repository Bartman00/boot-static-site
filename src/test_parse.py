import unittest

import parse
from textnode import TextNode, TextType


# Was using hard-coded maps instead of instructions to use an input
# for the delimiter.
class TestTextNode(unittest.TestCase):
    """
    def setUp(self) -> None:
        self.node = LeafNode("<p>", "a value",
                             props = {'k1':'v1', 'k2':'v2'})

    def test_check_delimiter(self):

        with self.assertRaises(ValueError):
            print(parse.check_delimiter("%"))
        self.assertIs(parse.check_delimiter("*"), None)

        self.assertEqual(self.node.tag, "p")
        self.assertEqual(self.node.value, "a value")
        self.assertEqual(self.node.props, {'k1':'v1', 'k2':'v2'})
    """

    def test_split_string_delimiter(self):

        text_string = "This is text with a `code block` word"
        delimiter = "`"
        result = parse.split_string_delimiter(text_string, delimiter, TextType.CODE)
        self.assertEqual(
            result,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_string_no_split(self):
        text_string = "This is text with a `code block` word"
        dont_split_me = parse.split_string_delimiter(text_string, "*", TextType.ITALIC)
        self.assertEqual(dont_split_me, [TextNode(text_string, TextType.TEXT)])

    def test_string_double_split(self):

        double_bold = "This string has **bold** and **another bold** text"
        db_result = parse.split_string_delimiter(double_bold, "**", TextType.BOLD)

        db_expect = [
            TextNode("This string has ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("another bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(db_result, db_expect)

    def test_string_assert(self):
        with self.assertRaises(ValueError):
            parse.split_string_delimiter("**unbalance", "**", TextType.BOLD)

    def test_string_blank(self):
        blank = parse.split_string_delimiter("", "*", TextType.TEXT)
        self.assertEqual(blank, TextNode("", TextType.TEXT))

    # ------------------------------------------------
    # Tests for the split_nodes_delimiter function
    # ------------------------------------------------
    def test_split_nodes_delimiter(self):

        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = parse.split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_nodes_start_delimiter(self):

        node = TextNode("`code` word", TextType.TEXT)
        new_nodes = parse.split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("code", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_nodes_end_delimiter(self):

        node = TextNode("word `code`", TextType.TEXT)
        new_nodes = parse.split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("word ", TextType.TEXT),
                TextNode("code", TextType.CODE),
            ],
        )

    def test_nodes_double_split(self):

        double_bold = TextNode(
            "This string has **bold** and **another bold** text", TextType.TEXT
        )
        db_result = parse.split_nodes_delimiter([double_bold], "**", TextType.BOLD)

        db_expect = [
            TextNode("This string has ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("another bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(db_result, db_expect)

    def test_nodes_do_nothing(self):

        node = TextNode("**already bolded**", TextType.BOLD)
        nodes = parse.split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(nodes, [TextNode("**already bolded**", TextType.BOLD)])

    def test_nodes_empty(self):
        nodes = parse.split_nodes_delimiter([], "**", TextType.TEXT)
        self.assertEqual(nodes, [])

    def test_nodes_multiple(self):

        double_bold = TextNode(
            "This string has **bold** and **another bold** text", TextType.TEXT
        )

        code = TextNode("This is some text with `code` in it", TextType.TEXT)
        already_bold = TextNode("**already bolded**", TextType.BOLD)

        node_list = [double_bold, code, already_bold]

        initial_expected = [
            TextNode("This string has ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("another bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
            TextNode("This is some text with `code` in it", TextType.TEXT),
            TextNode("**already bolded**", TextType.BOLD),
        ]

        initial_result = parse.split_nodes_delimiter(node_list, "**", TextType.BOLD)
        self.assertEqual(initial_result, initial_expected)

        expected = [
            TextNode("This string has ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("another bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
            TextNode("This is some text with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" in it", TextType.TEXT),
            TextNode("**already bolded**", TextType.BOLD),
        ]

        result = parse.split_nodes_delimiter(initial_result, "`", TextType.CODE)

        self.assertEqual(result, expected)

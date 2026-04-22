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
        
        double_bold = TextNode("**bold one****bold two", TextType.TEXT)
        with self.assertRaises(ValueError):
            print(parse.split_nodes_delimiter([double_bold], "**", TextType.BOLD))

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
        
    def test_extract_markdown_images(self):

        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"

        result = parse.extract_markdown_images(text)

        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]

        self.assertEqual(result, expected)
        
        empty_text = "This text does not have any links"
        empty_expect = []

        result = parse.extract_markdown_images(empty_text)
        self.assertEqual(result, empty_expect)

        matches = parse.extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

        almost = "This is text with [almost](all of the parts) of an image, but it [should](be empty)"
        result = parse.extract_markdown_images(almost)
        self.assertEqual(result, empty_expect)
        
    def test_extract_markdown_links(self):

        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"

        expected = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]

        result = parse.extract_markdown_links(text)
        self.assertEqual(result, expected)
        
        images_only = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"

        empty_result = []

        result = parse.extract_markdown_links(images_only)
        self.assertEqual(result, empty_result)
        

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = parse.split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
        
        no_image = TextNode("This is text without images", TextType.TEXT)

        no_image_nodes = parse.split_nodes_image([no_image])
        self.assertEqual(
                [
                    TextNode("This is text without images", TextType.TEXT)
                ],
                no_image_nodes
            )
            
        start_image = TextNode(
                "![another image](https://fakewebsite.com) other text", TextType.TEXT,
                )
        start_image_nodes = parse.split_nodes_image([start_image])
        self.assertEqual([
            TextNode("another image", TextType.IMAGE, "https://fakewebsite.com"),
            TextNode(" other text", TextType.TEXT)
            ], start_image_nodes
         )
         
        has_a_link = TextNode("[url text](https://www.boot.dev) doesn't actually have images", TextType.TEXT)
        link_nodes = parse.split_nodes_image([has_a_link])
        self.assertEqual([has_a_link], link_nodes)
        
        # Empty list should return an empty list
        self.assertEqual([], parse.split_nodes_image([]))
        

        # Start with multiple
        multi = [TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT),
                 TextNode("This also has ![images](fakelink.com) in it", TextType.TEXT)]

        expected = [TextNode("This is text with an ", TextType.TEXT),
                    TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                    TextNode(" and another ", TextType.TEXT),
                    TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"), 
                    TextNode("This also has ", TextType.TEXT),
                    TextNode("images", TextType.IMAGE, "fakelink.com"),
                    TextNode(" in it", TextType.TEXT)]
        self.assertEqual(parse.split_nodes_image(multi), expected)


        
    def test_split_links(self):

        has_a_link = TextNode("[url text](https://www.boot.dev) doesn't actually have images", TextType.TEXT)
        link_nodes = parse.split_nodes_link([has_a_link])
        self.assertEqual([
            TextNode("url text", TextType.LINK, "https://www.boot.dev"),
            TextNode(" doesn't actually have images", TextType.TEXT)
            ], link_nodes)

        combined = TextNode("[url text](www.google.com) has both links and ![images](www.image.com)", TextType.TEXT)
        combined_nodes = parse.split_nodes_link([combined])
        

        expected = [TextNode("url text", TextType.LINK, "www.google.com"),
                    TextNode(" has both links and ![images](www.image.com)", TextType.TEXT)
                    ]
        self.assertEqual(combined_nodes, expected)
        
        # Empty list should return an empty list
        self.assertEqual([], parse.split_nodes_link([]))
        

        # Start with multiple
        multi = [TextNode("This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)", TextType.TEXT),
                 TextNode("This also has [links](fakelink.com) in it", TextType.TEXT)]

        expected = [TextNode("This is text with an ", TextType.TEXT),
                    TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                    TextNode(" and another ", TextType.TEXT),
                    TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"), 
                    TextNode("This also has ", TextType.TEXT),
                    TextNode("links", TextType.LINK, "fakelink.com"),
                    TextNode(" in it", TextType.TEXT)]
        self.assertEqual(parse.split_nodes_link(multi), expected)
        
    def test_combined_split(self):
        # Combined
        self.assertEqual([], parse.combined_split(""))
        
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        
        result = parse.combined_split(text)

        self.assertEqual(result, expected)
        
        text = "**bold only**"
        expected = [TextNode("bold only", TextType.BOLD)]
        result = parse.combined_split(text)
        # print(f"{result=}")
        self.assertEqual(result, expected)
        
        text = "**bold one** **bold two**"
        expected = [TextNode("bold one", TextType.BOLD),
                    TextNode(" ", TextType.TEXT),
                    TextNode("bold two", TextType.BOLD)]
        result = parse.combined_split(text)
        self.assertEqual(result, expected)
        
        text = "![img1](website1)![img2](website2)"
        expected = [TextNode("img1", TextType.IMAGE, "website1"),
                    TextNode("img2", TextType.IMAGE, "website2")]
        result = parse.combined_split(text)
        self.assertEqual(result, expected)

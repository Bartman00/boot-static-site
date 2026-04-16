from textnode import TextNode, TextType
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):

    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            # Already parsed. Nested types not supported
            # print(f'Skipping: {old_node=}')
            new_nodes.append(old_node)
        else:
            new_nodes.extend(
                split_string_delimiter(old_node.text, delimiter, text_type)
            )
    return new_nodes


def split_string_delimiter(split_me, delimiter, text_type):
    # Handles a single string
    # print(f'{split_me=}')
    if split_me.count(delimiter) % 2 != 0:
        raise ValueError(f"{split_me} does not have balanced delimiters")
    if not text_type.is_valid(text_type):
        raise ValueError(f"{text_type} is invalid")

    ret = []

    if len(split_me) < 1:
        return TextNode("", text_type=TextType.TEXT)

    # Alternates between text and special text
    # This only starts with special if the first
    # character is the delimiter
    use_next = split_me[0] == delimiter
    split_up = split_me.split(delimiter)

    for isplit in split_up:
        if len(isplit) < 1:
            continue
        if use_next:
            # This block is the special type specified
            ret.append(TextNode(isplit, text_type=text_type))
        else:
            # Normal text
            ret.append(TextNode(isplit, text_type=TextType.TEXT))
        use_next = not use_next

    return ret
    
def extract_markdown_images(text):
    # Takes raw markdown text and returns a list of tuples
    # Each tuple contains (alt text, URL)
    regex = r"!\[.*?\]\(.*?\)"
    big_list = re.findall(regex, text)
    # print(f"big_list = {big_list}")
    
    ret = []
    
    for image in big_list:
        alt_text = re.findall(r"!\[.*?\]", image)
        alt_text = alt_text[0][2:-1]

        link = re.findall(r'\(.*?\)', image)
        link = link[0][1:-1]

        ret.append((alt_text, link))
    return ret

def extract_markdown_links(text):
    # Extracts links. Returns tuples of anchor text and URLs
    ret = []

    # Exclude ! becuase otherwise would match patterns from images
    regex = r"(?<!!)\[.*?\]\(.*?\)"
    big_list = re.findall(regex, text)
    
    for link in big_list:
        # print(f"{link=}")
        anchor = re.findall(r"\[.*?\]", link)
        anchor = anchor[0][1:-1]

        url = re.findall(r"\(.*?\)", link)
        url = url[0][1:-1]

        ret.append((anchor, url))

    return ret



if __name__ == "__main__":
    print("in parse.py")
    node = TextNode("This is text with a `code block` word", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    print(new_nodes)
    # Be sure to test:
    # 1. Starts with a delimiter
    # 2. Ends with a delimiter
    # 3. Multiple delimiters
    # 4. check_delimiter function
    # 5. split_string_delimiter function

    
    print("-------------------------------------------")

    double_bold = TextNode(
        "This string has **bold** and **another bold** text", TextType.TEXT
    )

    code = TextNode("This is some text with `code` in it", TextType.TEXT)
    already_bold = TextNode("**already bolded**", TextType.BOLD)

    node_list = [double_bold, code, already_bold]
    print("Printing node_list")
    for node in node_list:
        print(node)

    initial_expected = [
        TextNode("This string has ", TextType.TEXT),
        TextNode("bold", TextType.BOLD),
        TextNode(" and ", TextType.TEXT),
        TextNode("another bold", TextType.BOLD),
        TextNode(" text", TextType.TEXT),
        TextNode("This is some text with `code` in it", TextType.TEXT),
        TextNode("**already bolded**", TextType.BOLD),
    ]

    print("Printing result")
    initial_result = split_nodes_delimiter(node_list, "**", TextType.BOLD)
    for res in initial_result:
        print(res)
        
    
    print("-------------------------------------------")
    print("----EXTRACT_MARKDOWN_IMAGES----------------")
    text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    markdown_images = extract_markdown_images(text)

    for image in markdown_images:
        print(image)
        
        
    print("----EXTRACT_MARKDOWN_LINKS----------------")
    text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    links = extract_markdown_links(text)
    for link in links:
        print(link)
        
        
        

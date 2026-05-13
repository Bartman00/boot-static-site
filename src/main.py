from file_utilities import clear_folder, copy_files
from generate_page import generate_page_recursive
from textnode import TextNode, TextType


def main():
    test_node = TextNode(
        "This is some anchor text", TextType.LINK, "https://www.boot.dev"
    )
    print(test_node)

    print("----- Clearing old files -----")
    clear_folder("public")

    print("----- Copying static files -----")
    copy_files("static", "public")

    print("----- Generating pages -----")
    generate_page_recursive("content/", "template.html", "public/")


if __name__ == "__main__":
    main()

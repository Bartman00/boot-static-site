from textnode import TextNode, TextType
from file_utilities import copy_files

def main():
    test_node = TextNode(
        "This is some anchor text", TextType.LINK, "https://www.boot.dev"
    )
    print(test_node)
    
    print("Running file_utilities")
    copy_files("static", "public")
    



if __name__ == "__main__":
    main()

from file_utilities import clear_folder, copy_files
from generate_page import generate_page_recursive
import sys


def main():
    if len(sys.argv) > 1:
        # Includes a basepath
        basepath = sys.argv[1]
    else:
        basepath = "/"
    print(f"basepath: {basepath}")

    print("----- Clearing old files -----")
    clear_folder("docs")

    print("----- Copying static files -----")
    copy_files("static", "docs")

    print("----- Generating pages -----")
    generate_page_recursive("content/", "template.html", "docs/", basepath)


if __name__ == "__main__":
    main()

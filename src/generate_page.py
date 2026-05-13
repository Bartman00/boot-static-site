import re
from file_utilities import get_text_file, write_text_file, clear_folder
from md_to_html import markdown_to_html_node
import os

def extract_title(md):
    '''
    Returns header 1 string.

    Inputs:
    md(str): Markdown String

    Output:
    h1(str): Header 1 string

    Raieses:
    ValueError: No h1 title found
    '''

    pattern = r"^#\s(.+)"
    h1 = re.search(pattern, md, re.MULTILINE)

    if h1 is None:
        raise ValueError("Missing header 1 string")
    
    return h1.group(1).strip()

def generate_page(from_path, template_path, dest_path):
    '''
    Driver to generate html page
    '''

    # Print intro message
    print(f"Generating page {from_path} to {dest_path} using {template_path}")
    
    # Read markdown from_path
    print("Getting markdown")
    try:
        md = get_text_file(from_path)
    except Exception as e:
        print("Error getting markdown")
        print(e)
        return None

    # Read tempalte at template_path
    print("Getting template")
    try:
        template = get_text_file(template_path)
    except Exception as e:
        print("Error getting template")
        print(e)
        return None

    # Convert markdown to HTML string
    print("Convert to html")
    try:
        html = markdown_to_html_node(md).to_html()
    except Exception as e:
        print("Error converting md to html")
        print(e)
        return None

    # Get title
    print("Get title")
    try:
        title = extract_title(md)
    except Exception as e:
        print("Error getting title")
        print(e)
        return None

    # Replace placeholders in template
    print("Update template")
    try:
        new_content = template.replace("{{ Title }}", title)
        new_content = new_content.replace("{{ Content }}", html)
    except Exception as e:
        print("Error substituting text")
        print(e)
        return None

    # Write file at dest_path
    print("Write file")
    try:
        write_text_file(dest_path, new_content)
    except Exception as e:
        print("Error writing file")
        print(e)
        return None
        
    return new_content
    
    
def generate_page_recursive(dir_path_content, template_path, dest_dir_path):
    # Recursively generate all files starting with a seed
    
    cwd = os.getcwd()
    dir_folder = os.path.join(cwd, dir_path_content)
    dest_dir_path = os.path.join(cwd, dest_dir_path)

    if not os.path.exists(dir_folder):
        print(f"dir_folder: {dir_folder} does not exist")
        return None
        
    all_items = os.listdir(dir_folder)

    for item in all_items:
        from_path = os.path.join(dir_folder, item)
        to_path = os.path.join(dest_dir_path, item.replace(".md", ".html"))
        

        if os.path.isfile(from_path):
            # Copy
            generate_page(from_path, template_path, to_path)


        elif os.path.isdir(from_path):

            recursion_successful = generate_page_recursive(from_path, 
                                            template_path,
                                           to_path)
            
            if not recursion_successful:
                print("Error: recusive call failed.")
                return None
        
        else:
            # Shouldn't get here
            print("Error: generate_page_recursive item was neither a file nora folder.")
            return None
            
    return True

if __name__ == "__main__":
    md = "# Header 1"
    print(extract_title(md))
    

    print("\n\n----- Time to test the big one! -----\n")
    template = "template.html"
    md = "content/index.md"
    dest = r"test_folder/index.html"
    generate_page(md, template, dest)


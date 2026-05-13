import os
import shutil

def copy_files(source, destination, is_recursive=False):
    # Recursively copies files from a source
    # to a destination
    # Starts with current working directory
    
    log = "-----Recursive call------\n" if is_recursive else ""
    log += "Attempting to copy from\n"
    log += f"{source}\n"
    log += "to\n"
    log += f"{destination}\n"

    cwd = os.getcwd()
    log += f"\nCWD:\n{cwd}\n"
    
    source = os.path.join(cwd, source)
    destination = os.path.join(cwd, destination)
    clear_folder(destination)
    
    # Check that path exists
    if not os.path.exists(source):
        log += f"Could not find:\n{source}"
        save_log(log, "copy_log.txt")
        raise FileNotFoundError(f"Source not found:\n{source}")
    if not os.path.exists(destination):
        raise FileNotFoundError(f"Destination not found:\n{destination}")
    
    # Get list of files and folders
    all_items = os.listdir(source)
    

    log += f"\nFound {source} source directory"
    log += f"\nFound {destination} destination directory"
    
    # Loop through them
    # print("All items:")
    for item in all_items:
        log += f"\n\nItem: {item}:"
        full_path = os.path.join(source, item)
        if os.path.isfile(full_path):
            # copy from source to destination
            log += "\nIs a file."
            new_file = os.path.join(destination, item)
            shutil.copy(full_path, new_file)
            log += f"\nCopied from:\n{full_path}"
            log += f"\nCopied to:\n{new_file}"
        else:
            # Create a folder in destination
            # Add folder name to source and destination
            # recursively call this function
            log += "\nIs a folder."
            new_directory = os.path.join(destination, item)
            os.mkdir(new_directory)
            
            
            res = copy_files(full_path, new_directory, True)

            if not res:
                return False
            else:
                # Returned a log
                log += "\n" + res
                log += f"\nCopied folder from:\n{full_path}"
                log += f"\nTo:\n{new_directory}"

    if not is_recursive:
        log += "\n\n------Saving log------"
        save_log(log, "copy_log.txt")
    else:
        log += "\n------Returning Recursive Log------"
        return log

def save_log(log_string, filename, print_log=False):

    with open(filename, "w") as file:
        file.write(log_string)
        
    if print_log:
        print(log_string)

def clear_folder(folder):
    # Deletes all items in a folder recursively
    
    # Don't want to remove the directory itself

    cwd = os.getcwd()
    
    folder = os.path.join(cwd, folder)

    # Check that path exists
    if not os.path.exists(folder):
        raise FileNotFoundError(f"Source not found:\n{folder}")
    
    # Get list of files and folders
    all_items = os.listdir(folder)
    
    for item in all_items:
        full_path = os.path.join(folder, item)
        if os.path.isfile(full_path):
            # Delete
            os.remove(full_path)
        
        else:
            # Delete entire direcory
            shutil.rmtree(full_path)

    
def get_text_file(filepath):
    # Returns text content if found.
    # Raises an exception if not.

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Can't find:\n{filepath}")
    
    if not os.path.isfile(filepath):
        raise ValueError(f"Not a file: \n{filepath}")
        
    with open(filepath, "r") as file:
        content = file.read()
    return content.strip()
    
def write_text_file(filepath, content):
    # Writes to a file

    parent = os.path.dirname(filepath)
    
    if not parent:
        raise ValueError("parent directory does not exist")

    if not os.path.exists(parent):
        os.makedirs(parent, exist_ok=True)
        
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)


if __name__ == "__main__":
    # print("In file_utilities\n")
    # print(f"Working directory:\n{os.getcwd()}\n")
    # print(f"copy_files: {copy_files("static", "public")}\n")
    # clear_folder("public")
    result = get_text_file("template.html")
    print(result)
    expected = """<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{{ Title }}</title>
    <link href="/index.css" rel="stylesheet" />
  </head>

  <body>
    <article>{{ Content }}</article>
  </body>
</html>"""
    print("----------")
    i = 298
    print(f"expected length = {len(expected)}")
    print(f"result length = {len(result)}")
    print(expected[:i])
    print(result[:i] == expected[:i])

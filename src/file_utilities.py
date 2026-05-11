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

    

if __name__ == "__main__":
    print("In file_utilities\n")
    print(f"Working directory:\n{os.getcwd()}\n")
    print(f"copy_files: {copy_files("static", "public")}\n")
    # clear_folder("public")

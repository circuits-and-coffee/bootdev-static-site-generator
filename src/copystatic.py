import os
import shutil

def copy_files_recursive(source_dir, destination_dir):
    # Write a recursive function that copies all the contents from a source directory
    # to a destination directory (in our case, static to public)
    current_dir = os.curdir
    
    contents = os.listdir(source_dir) # Items in `contents` could be folders or files
    for item in contents:
        full_path_of_item = os.path.join(current_dir,source_dir,item)
        if not os.path.isfile(full_path_of_item):
            new_destination_dir = os.path.join(current_dir,destination_dir,item)
            # Need to go through this folder
            os.makedirs(new_destination_dir)
            copy_files_recursive(full_path_of_item,new_destination_dir)
        else:
            shutil.copy(full_path_of_item,destination_dir)
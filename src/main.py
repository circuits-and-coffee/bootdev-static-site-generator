import os
import shutil
from copystatic import copy_files_recursive
from gencontent import generate_pages_recursive

def main():

    # Initialize
    source_dir = "./static"
    public_dir = "./public"
    dir_path_content = "./content"
    template_path = "./template.html"
    
    # Clean public directory
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
    
    # Copy files
    copy_files_recursive(source_dir,public_dir)
    
    # Generate all pages!    
    generate_pages_recursive(dir_path_content, template_path, public_dir) # Source directory, template path, destination (public) directory

if __name__ == "__main__":
    main()
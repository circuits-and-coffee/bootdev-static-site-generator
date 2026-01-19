import os
import shutil
from copystatic import copy_files_recursive
from gencontent import generate_pages_recursive
import sys

def main():
    
    basepath = sys.argv[1] if len(sys.argv)>1 else "/"

    # Initialize
    source_dir = "static"
    docs_dir = "docs"
    dir_path_content = "content"
    template_path = "template.html"
    
    # Clean destination directory
    if os.path.exists(docs_dir):
        shutil.rmtree(docs_dir)
    
    # Copy files
    copy_files_recursive(source_dir,docs_dir)
    
    # Generate all pages!    
    generate_pages_recursive(dir_path_content, template_path, docs_dir, basepath) # Source directory, template path, destination (public) directory

if __name__ == "__main__":
    main()
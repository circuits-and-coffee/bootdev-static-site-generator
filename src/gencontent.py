import os
from operations import *
from textnode import *
from htmlnode import *

def extract_title(markdown):
    # Find the line with an "#h1" tag
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if (block_to_block_type(block) == BlockType.HEADING and block.startswith("# ")):
            return block[1:].strip()
    raise Exception("No header detected")

def generate_page(from_path, template_path, dest_file_path, basepath):
    print(f"Generating page from {from_path} to {dest_file_path} using {template_path}.")
    input_file = open(from_path)
    md = input_file.read()
    template_file = open(template_path)
    template = template_file.read()
    
    # Convert markdown to HTML
    html = markdown_to_html_node(md).to_html()
    title = extract_title(md)
    
    # Replace the {{ Title }} and {{ Content }} placeholders in the template with the HTML and title you generated.
    template = template.replace("{{ Content }}",html).replace("{{ Title }}", title)
    template = template.replace('href="/', f'"href="{basepath}"')
    template = template.replace('src="/', f'"src="{basepath}"')
    if not os.path.exists(os.path.dirname(dest_file_path)):
        # Need to make the dir:
        os.makedirs(os.path.dirname(dest_file_path))
    
    with open(dest_file_path, "w") as file:
        file.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    # Write a recursive function that copies all the contents from a source directory
    # to a destination directory (in our case, static to public)

    contents = os.listdir(dir_path_content) # Items in `contents` could be folders or files
    for item in contents:
        full_path_of_item = os.path.join(dir_path_content, item)
        if os.path.isdir(full_path_of_item):
            # Recursively call this function from this new directory
            new_base_dir, _ = os.path.splitext(item) 
            new_dest_dir = os.path.join(dest_dir_path,new_base_dir)
            generate_pages_recursive(full_path_of_item,template_path,new_dest_dir, basepath)
        else:
            # This is a file we need to convert!
            filename, ext = os.path.splitext(item)
            if ext == ".md":
                file_changed_extension = filename + ".html" # Change file extension
                original_filename = os.path.join(dir_path_content,item)
                new_filename = os.path.join(dest_dir_path, file_changed_extension)
                
                # Call generate_page()
                generate_page(original_filename,template_path,new_filename, basepath)

if __name__ == '__main__':
    generate_page("content/index.md","template.html","public/index.html")
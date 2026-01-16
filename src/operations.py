import re
from blocktype import *
from htmlnode import *
from textnode import *
from operations import *

# Jan 14th - Working on this method (and its helper methods)
def markdown_to_html_node(markdown):
    # Converts a full markdown document (string) into a single parent HTMLNode (with a lot of children HTMLNodes)
    
    output_html = ParentNode('div',[]) # This is what we'll return at the very end with our children HTMLNodes
    
    markdown_blocks = markdown_to_blocks(markdown)
    
    for block in markdown_blocks:
        # Need to determine what kind of block this is
        block_type = block_to_block_type(block)
        
        if block_type == (BlockType.PARAGRAPH):
            lines = block.split("\n")
            new_lines = " ".join(lines)
            inline_children = text_to_html_children(new_lines)
            paragraph_node = ParentNode('p', inline_children)
            output_html.children.append(paragraph_node)
            
        elif block_type == (BlockType.HEADING):
            heading_level = block.count("#")
            cleaned_heading = block[heading_level:].strip()
            inline_children = text_to_html_children(cleaned_heading)
            header_node = ParentNode(f'h{heading_level}',inline_children)
            output_html.children.append(header_node)
            
        if block_type == BlockType.CODE:
            lines = block.split("\n")
            inner_lines = lines[1:-1]
            combined_code = "\n".join(inner_lines) + "\n"
            code_node = LeafNode('code', combined_code)
            pre_node = ParentNode('pre', [code_node])
            output_html.children.append(pre_node)
            
        elif block_type == BlockType.QUOTE:
            lines = block.split("\n")
            combined_lines = " ".join(lines).replace("> ","")
            inline_children = text_to_html_children(combined_lines)
            paragraph_node = ParentNode('p', inline_children)
            blockquote_node = ParentNode('blockquote',[paragraph_node])
            output_html.children.append(blockquote_node)

        elif block_type == BlockType.ORDERED_LIST:
            list_node = ParentNode('ol',[])
            
            lines = block.split("\n")
            cleaned_lines = [line[2:].strip() for line in lines]
            for line in cleaned_lines:
                html_child = text_to_html_children(line)
                li_node = ParentNode("li", html_child)
                list_node.children.append(li_node)
                
            output_html.children.append(list_node)
        
        elif block_type == BlockType.UNORDERED_LIST:
            list_node = ParentNode('ul',[])
            
            lines = block.split("\n")
            cleaned_lines = [line[1:].strip() for line in lines]
            for line in cleaned_lines:
                html_child = text_to_html_children(line)
                li_node = ParentNode("li", html_child)
                list_node.children.append(li_node)
                
            output_html.children.append(list_node)
    
    html = output_html.to_html()
    return output_html



def text_to_html_children(text):
    ###
    # Takes a string of text and returns a list of HTMLNodes
    # that represent the inline markdown using previously created
    # functions (think TextNode -> HTMLNode)
    ###
    text_nodes = text_to_textnodes(text)
    html_children = [text_node_to_html_node(tn) for tn in text_nodes]
    return html_children
            
def format_markdown(text_lines):
    # Go through each line and apply formatting? But what if one line has multiple formats?
    for string in text_lines:
        pass
    
            
# This may not have been needed, but I made it and I want to keep it just in case :^)
def paragraph_generator(markdown):
    line_by_line_md = markdown.split("\n")
    final_md_list = []
    temp_node = []
    for line in line_by_line_md:
        if line == '':
            # If temp_node is populated, move it into final_md_list and reset it
            if len(temp_node) > 0:
                final_md_list.append(' '.join(temp_node))
                temp_node = []
        else:
            # We're appending to the last temp_node
            temp_node.append(line)
    return final_md_list

def split_nodes_image(old_nodes):
    output_nodes = []
    
    for old_node in old_nodes:
        remaining_text = old_node.text
        images = extract_markdown_images(remaining_text)

        if old_node.text_type != TextType.TEXT:
            output_nodes.append(old_node)
            continue
        elif images == []:
            output_nodes.append(old_node)
            continue
        else:
            for alt_text, image in images:
                markdown = f"![{alt_text}]({image})"
                before, after = remaining_text.split(markdown, 1)
                if before != "":
                    output_nodes.append(TextNode(before, TextType.TEXT))
                output_nodes.append(TextNode(alt_text,TextType.IMAGE, image))
                remaining_text = after
            if remaining_text != "":
                output_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return output_nodes

def split_nodes_link(old_nodes):
    output_nodes = []
    
    for old_node in old_nodes:
        # Run our extraction function
        remaining_text = old_node.text
        links = extract_markdown_links(remaining_text)

        if old_node.text_type != TextType.TEXT:
            output_nodes.append(old_node)
            continue
        elif links == []:
            # No links here
            output_nodes.append(TextNode(old_node.text,TextType.TEXT))
            continue
        else:
            
            for alt_text, link in links:
                
                markdown = f"[{alt_text}]({link})"
                before, after = remaining_text.split(markdown, 1)

                if before != "":
                    output_nodes.append(TextNode(before, TextType.TEXT))
                output_nodes.append(TextNode(alt_text,TextType.LINK, link))
                remaining_text = after
            if remaining_text != "":
                output_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return output_nodes

def text_to_textnodes(text):
    
    # What happens if we just make a TextNode out of this string?
    text_node_to_manipulate = TextNode(text,TextType.TEXT)
    split_up_images = split_nodes_image([text_node_to_manipulate])
    split_up_images_and_links = split_nodes_link(split_up_images)
    
    # Now we'll have an array of Markdown text nodes (that need formatting), image TextNodes, and link TextNodes
    delimiters = [("**",TextType.BOLD),("`",TextType.CODE),('_',TextType.ITALIC)]
    nodes_to_modify = split_up_images_and_links
    for delimiter in delimiters:
        nodes_to_modify = split_nodes_delimiter(nodes_to_modify,delimiter[0],delimiter[1])
    return nodes_to_modify

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    image_regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    images = re.findall(image_regex, text)
    return images

def extract_markdown_links(text):
    link_text_regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    links = re.findall(link_text_regex, text)
    return links


def markdown_to_blocks(markdown):
    # Separate incoming markdown into a list separated by newline characters
    output_blocks = []
    segmented_markdown = markdown.split('\n\n')
    for segment in segmented_markdown:
        cleaned_segment = segment.strip()
        if cleaned_segment != "":
            # Not empty, let's parse it
            output_blocks.append(cleaned_segment)
    return output_blocks

        

if __name__ == "__main__":
    
    #Simple paragraph markdown test
#     markdown = """
# This is a regular paragraph 
# nothing unusual going on here
# ...but formatting is fine, _right_?
# """

    #Blockquote markdown test
    markdown = """
> This is a block quote 
> or at least I'm _hoping_...
> ...I think **this** is right?
"""

    # Code block markdown test
#     markdown = """
# ```
# This is text that _should_ remain
# the **same** even with inline stuff
# ```
# """
    markdown_to_html_node(markdown)
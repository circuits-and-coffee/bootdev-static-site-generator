import re
from textnode import *
from operations_html import *
from operations_markdown import *

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
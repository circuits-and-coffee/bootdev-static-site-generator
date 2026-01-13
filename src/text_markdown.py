import re
from textnode import *

# def split_nodes_delimiter(old_nodes, delimiter, text_type):
#     new_nodes = []
#     for old_node in old_nodes:
#         if old_node.text_type != TextType.TEXT:
#             new_nodes.append(old_node)
#             continue
#         split_nodes = []
#         sections = old_node.text.split(delimiter)
#         if len(sections) % 2 == 0:
#             raise ValueError("invalid markdown, formatted section not closed")
#         for i in range(len(sections)):
#             if sections[i] == "":
#                 continue
#             if i % 2 == 0:
#                 split_nodes.append(TextNode(sections[i], TextType.TEXT))
#             else:
#                 split_nodes.append(TextNode(sections[i], text_type))
#         new_nodes.extend(split_nodes)
#     return new_nodes


# def split_nodes_image(old_nodes):
#     new_nodes = []
#     for old_node in old_nodes:
#         if old_node.text_type != TextType.TEXT:
#             new_nodes.append(old_node)
#             continue
#         original_text = old_node.text
#         images = extract_markdown_images(original_text)
#         if len(images) == 0:
#             new_nodes.append(old_node)
#             continue
#         for image in images:
#             sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
#             if len(sections) != 2:
#                 raise ValueError("invalid markdown, image section not closed")
#             if sections[0] != "":
#                 new_nodes.append(TextNode(sections[0], TextType.TEXT))
#             new_nodes.append(
#                 TextNode(
#                     image[0],
#                     TextType.IMAGE,
#                     image[1],
#                 )
#             )
#             original_text = sections[1]
#         if original_text != "":
#             new_nodes.append(TextNode(original_text, TextType.TEXT))
#     return new_nodes


# def split_nodes_link(old_nodes):
#     new_nodes = []
#     for old_node in old_nodes:
#         if old_node.text_type != TextType.TEXT:
#             new_nodes.append(old_node)
#             continue
#         original_text = old_node.text
#         links = extract_markdown_links(original_text)
#         if len(links) == 0:
#             new_nodes.append(old_node)
#             continue
#         for link in links:
#             sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
#             if len(sections) != 2:
#                 raise ValueError("invalid markdown, link section not closed")
#             if sections[0] != "":
#                 new_nodes.append(TextNode(sections[0], TextType.TEXT))
#             new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
#             original_text = sections[1]
#         if original_text != "":
#             new_nodes.append(TextNode(original_text, TextType.TEXT))
#     return new_nodes


# def extract_markdown_images(text):
#     pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
#     matches = re.findall(pattern, text)
#     return matches


# def extract_markdown_links(text):
#     pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
#     matches = re.findall(pattern, text)
#     return matches

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
    output_matches = []

    image_regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    
    images = re.findall(image_regex, text)
    return images

def extract_markdown_links(text):
    output_matches = []

    link_text_regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    links = re.findall(link_text_regex, text)
    return links

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
    # test_node = TextNode(
    #         "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
    #         TextType.TEXT,
    #     )
    # split_nodes_link([test_node])
    # text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    # text_to_textnodes(text)
    md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""

    markdown_to_blocks(md)
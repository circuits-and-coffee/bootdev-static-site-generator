import re
from textnode import *
from operations_html import *

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
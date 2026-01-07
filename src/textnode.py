from enum import Enum
from htmlnode import HTMLNode

class TextType(Enum):
    TEXT = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        # Check each object's attributes
        return (self.text == other.text and
                self.text_type == other.text_type and
                self.url == other.url)
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    
def text_node_to_html_node(text_node):
    if text_node.text_type not in TextType:
        raise Exception
    
    if text_node.text_type == TextType.TEXT:
        return HTMLNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return HTMLNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return HTMLNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return HTMLNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return HTMLNode("a", text_node.text, None, ["href"])
    elif text_node.text_type == TextType.IMAGE:
        return HTMLNode("img", text_node.text,None, ["src","alt"])
    return

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    output_nodes = []
    for node in old_nodes:
        # Check if it's a TextNode        
        if node.text_type == TextType.TEXT:
            # Check for delimiters
            # print(f"Delimiter count: {node.text.count(delimiter)}")
            segments = node.text.split(delimiter)
            if len(segments) % 2 == 0:
                # Wrong number of delimiters
                raise Exception("Odd number of delimiters, invalid markdown")
                
            for i in range(len(segments)):
                if segments[i] == "":
                    continue
                if i % 2 == 0:
                    # This is the middle split, which means it's the formatted text!
                    output_nodes.append(TextNode(segments[i],TextType.TEXT))
                else:
                    output_nodes.append(TextNode(segments[i],text_type))
                
                
                
            # if node.text.count(delimiter) == 0:
            #     # No delimiter, just treat it as regular text
            #     output_nodes.append(node)
            
            # else:
            #     # Get position of first delimiter
            #     idx_first_delimiter = node.text.find(delimiter)
                
            #     # Break the text into plain text and formatted text
            #     segments = node.text.split(delimiter)
            #     for segment in segments:
            #         print(f"Current segment is '{segment}'")
            #         # See if start of this segment matches the start of the first delimiter
            #         idx_segment = node.text.find(segment)
            #         if idx_first_delimiter + 1 == idx_segment:
            #             # This is the one!
            #             output_nodes.append(TextNode(segment,text_type))
            #             pass
            #         else:
            #             # Just a regular old text node
            #             output_nodes.append(TextNode(segment,TextType.TEXT))
                        
    return output_nodes    
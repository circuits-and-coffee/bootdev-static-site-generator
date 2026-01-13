from enum import Enum
import re
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

    
    

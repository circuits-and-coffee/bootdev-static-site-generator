from enum import Enum
import re

class BlockType(Enum):
    paragraph = "paragraph"
    heading = "heading"
    code = "code"
    quote = "quote"
    unordered_list = "unordered_list"
    ordered_list = "ordered_list"


def block_to_block_type(markdown_text_block):
    lines = markdown_text_block.split("\n")
    
    # Check if it's heading
    if lines[0].startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.heading
    
    # Check if it's code
    if lines[0] == "```":
        if lines[-1] == "```":
            return BlockType.code
        else:
            return BlockType.paragraph
    
    if lines[0].startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.paragraph
        return BlockType.quote
    elif lines[0].startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.paragraph
        return BlockType.unordered_list
    elif lines[0].startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.paragraph
            i += 1
        return BlockType.ordered_list
    else:
        return BlockType.paragraph

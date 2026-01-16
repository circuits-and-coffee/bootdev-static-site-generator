import unittest
from blocktype import *
from textnode import *
from operations import *
from operations import *

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        
    def test_not_eq_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
        
    def test_not_eq_link(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC,'https://example.com')
        self.assertNotEqual(node, node2)
    
    def test_not_eq_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a link", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_repr(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(repr(node1), "TextNode(This is a text node, TextType.BOLD, None)")
        
        
    """
    Tests for functions
    """
    def test_text_plain(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        
    def test_text_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")
        
    def test_text_italic(self):
        node = TextNode("This is a italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a italic node")
        
    def test_text_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")
        
    def test_text_link(self):
        node = TextNode("This is a link node", TextType.LINK)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props, ["href"])
        self.assertEqual(html_node.value, "This is a link node")
        
    def test_text_image(self):
        node = TextNode("", TextType.IMAGE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props, ["src","alt"])
        self.assertEqual(html_node.value, "")
        
    def test_text_delimiting_middle(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        formatted_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, formatted_nodes)

    def test_text_delimiting_start(self):
        node = TextNode("*This* sentence starts with bold text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.BOLD)
        formatted_nodes = [
            TextNode("This", TextType.BOLD),
            TextNode(" sentence starts with bold text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, formatted_nodes)
        
    def test_text_multiple_sections(self):
        node = TextNode("This sentence _looks_ to be formated properly...and that's because _it is!_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        formatted_nodes = [
            TextNode("This sentence ", TextType.TEXT),
            TextNode("looks", TextType.ITALIC),
            TextNode(" to be formated properly...and that's because ", TextType.TEXT),
            TextNode("it is!", TextType.ITALIC)
        ]
        self.assertEqual(new_nodes, formatted_nodes)
        
    def test_all_text_formatted(self):
        node = TextNode("*WOW, AMAZING!*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.BOLD)
        formatted_nodes = [
            TextNode("WOW, AMAZING!", TextType.BOLD)
        ]
        self.assertEqual(new_nodes, formatted_nodes)
        
    def test_unformatted_text(self):
        node = TextNode("Wow. Amazing.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.BOLD)
        formatted_nodes = [
            TextNode("Wow. Amazing.", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, formatted_nodes)
        
        
    def test_text_invalid_markdown(self):
        node = TextNode("This sentence _looks to be formated properly, but...", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "_", TextType.ITALIC)
            
    def test_text_markdown_image_extraction(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        extracted_text = extract_markdown_images(text)
        expected_text = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(extracted_text,expected_text)
        
    def test_metadata_regex(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        extracted_text = extract_markdown_links(text)
        expected_text = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(extracted_text,expected_text)
        
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://amazon.com)"
        )
        self.assertListEqual([("link", "https://amazon.com")], matches)
        
        
    def test_split_markdown(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected_nodes = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertEqual(new_nodes, expected_nodes)
        
        
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected_nodes = [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ]
        self.assertListEqual(expected_nodes,new_nodes)
        
    def test_split_nodes_link_multiple_links(self):
        node = TextNode(
            "a [one](https://1.com) b [two](https://2.com) c",
            TextType.TEXT,
        )

        result = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("a ", TextType.TEXT),
                TextNode("one", TextType.LINK, "https://1.com"),
                TextNode(" b ", TextType.TEXT),
                TextNode("two", TextType.LINK, "https://2.com"),
                TextNode(" c", TextType.TEXT),
            ],
            result,
        )
        
    def test_split_nodes_image_multiple_images(self):
        node = TextNode(
            "a ![one](https://1.png) b ![two](https://2.png) c",
            TextType.TEXT,
        )

        result = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("a ", TextType.TEXT),
                TextNode("one", TextType.IMAGE, "https://1.png"),
                TextNode(" b ", TextType.TEXT),
                TextNode("two", TextType.IMAGE, "https://2.png"),
                TextNode(" c", TextType.TEXT),
            ],
            result,
        )
        
    def test_split_empty_links(self):
        node = TextNode(
            "This text node doesn't actually have any links...whoops",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node],new_nodes)
    
    def test_split_empty_images(self):
        node = TextNode(
            "This text node doesn't actually have any images...whoops",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node],new_nodes)
        
    def test_complete_text_conversion(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        converted_text = text_to_textnodes(text)
        expected_response = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(converted_text, expected_response)
        
    def test_complete_text_conversion_only_bold(self):
        text = "**OOPS THIS IS ALL BOLD!!**"
        converted_text = text_to_textnodes(text)
        expected_response = [
            TextNode("OOPS THIS IS ALL BOLD!!", TextType.BOLD),
        ]
        self.assertEqual(converted_text, expected_response)
        
    ### Markdown block tests
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_markdown_empty(self):
        md = """
    This is **bolded** paragraph


    - with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "- with items",
            ],
        )
        
    def test_blocktype_codeblock(self):
        block = "\n".join([
    "```",
    "This is a code snippet (I think)",
    "It was probably said by someone really smart",
    "And is crazy deep if you think about it",
    "```"
])
        blockType = block_to_block_type(block)
        self.assertEqual(blockType, BlockType.CODE)
        
    def test_blocktype_blockquote(self):
        block = "\n".join([
    "> This is a block quote",
    "> It was probably said by someone really smart",
    "> And is crazy deep if you think about it",
])
        blockType = block_to_block_type(block)
        self.assertEqual(blockType, BlockType.QUOTE)
        
    def test_blocktype_unorderedlist(self):
        block = "\n".join([
    "- This is an unordered list",
    "- You can tell cause there aren't any numbers in the front",
    "- Pretty straightforward innit",
])
        blockType = block_to_block_type(block)
        self.assertEqual(blockType, BlockType.UNORDERED_LIST)
    
    def test_blocktype_orderedlist(self):
        block = "\n".join([
    "1. This is an ordered list",
    "2. It's got numbers",
    "3. This format would have been nice to know before doing the lesson...",
])
        blockType = block_to_block_type(block)
        self.assertEqual(blockType, BlockType.ORDERED_LIST)
        
if __name__ == "__main__":
    unittest.main()
import unittest
from textnode import *

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

if __name__ == "__main__":
    unittest.main()
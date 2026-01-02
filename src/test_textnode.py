import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        # print("Testing if this works via test.sh")
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

if __name__ == "__main__":
    unittest.main()
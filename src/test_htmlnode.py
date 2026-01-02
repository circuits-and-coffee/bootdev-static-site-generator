import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_html_conversion_paragraph(self):
        test_props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        paragraph_node = HTMLNode("p","Test paragraph.",None,test_props)
        para_html_conversion = HTMLNode.props_to_html(paragraph_node)
        self.assertEqual(' href="https://www.google.com" target="_blank"',para_html_conversion)
        
    def test_html_conversion_one_prop(self):
        test_prop = {"href": "https://www.google.com"}
        paragraph_node = HTMLNode("p","Test paragraph.",None,test_prop)
        para_html_conversion = HTMLNode.props_to_html(paragraph_node)
        self.assertEqual(' href="https://www.google.com"',para_html_conversion)
        
    def test_repr(self):
        paragraph_node = HTMLNode("p","Test paragraph.",None,None)
        expected_output = f"HTMLNode({paragraph_node.tag}, {paragraph_node.value}, children: {paragraph_node.children}, {paragraph_node.props})"
        self.assertEqual(f"{paragraph_node}",expected_output)
        
    def test_parent_element_repr(self):
        test_props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        paragraph_node = HTMLNode("p","Test paragraph.",None,None)
        header_node = HTMLNode("h1","Header One",[paragraph_node],test_props)
        expected_output = f"HTMLNode({header_node.tag}, {header_node.value}, children: {header_node.children}, {header_node.props})"
        self.assertEqual(f"{header_node}",expected_output)
        
if __name__ == '__main__':
    unittest.main()
    
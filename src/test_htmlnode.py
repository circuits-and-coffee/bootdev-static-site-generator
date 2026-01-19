import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode
from operations import *

class TestHTMLNode(unittest.TestCase):
    
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>',
        )

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )
        
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
        
    def test_leaf_to_html_p(self):
        node = LeafNode("p", 'Hello, world!')
        self.assertEqual(node.to_html(), '<p>Hello, world!</p>')
        
    def test_leaf_to_html_link(self):
        test_props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = LeafNode("h1","Header One",test_props)
        self.assertEqual(node.to_html(), '<h1 href="https://www.google.com" target="_blank">Header One</h1>')
    
    def test_leaf_to_html_raw(self):
        node = LeafNode(None, 'Hello, world!')
        self.assertEqual(node.to_html(), 'Hello, world!')
        
        
    # ParentNode Tests
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
        
    def test_to_html_without_children_error(self):
        parent_node = ParentNode("div", None)
        self.assertRaises(ValueError, parent_node.to_html)

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
    )
        
        
    # Markdown to HTML Tests (The Big Ones)
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )
        
    def test_convert_heading(self):
        md = "### Tier 3 Heading (**Exciting!**)"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h3>Tier 3 Heading (<b>Exciting!</b>)</h3></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
        
        
    def test_convert_quoteblock(self):
        markdown = """
> This is a block quote
> or at least I'm _hoping_...
> ...I think **this** is right?
"""
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a block quote\nor at least I'm <i>hoping</i>...\n...I think <b>this</b> is right?</blockquote></div>"
        )
        
    def test_convert_unordered_list(self):
        markdown = """
- This is a simple list
- There's some **flare** in this list!
- How crazy is that?
"""
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a simple list</li><li>There's some <b>flare</b> in this list!</li><li>How crazy is that?</li></ul></div>"
        )
        
    def test_convert_ordered_list(self):
        markdown = """
1. first **item**
2. second _item_
3. third
"""
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>first <b>item</b></li><li>second <i>item</i></li><li>third</li></ol></div>"
        )
        
        
    def test_super_complicated_markdown_to_html(self):
        markdown = """
# Tolkien Fan Club

![JRR Tolkien sitting](/images/tolkien.png)

Here's the deal, **I like Tolkien**.

> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien

## Blog posts

- [Why Glorfindel is More Impressive than Legolas](/blog/glorfindel)
- [Why Tom Bombadil Was a Mistake](/blog/tom)
- [The Unparalleled Majesty of "The Lord of the Rings"](/blog/majesty)

## Reasons I like Tolkien

- You can spend years studying the legendarium and still not understand its depths
- It can be enjoyed by children and adults alike
- Disney _didn't ruin it_ (okay, but Amazon might have)
- It created an entirely new genre of fantasy
        """
        expected_html = """<div><h1>Tolkien Fan Club</h1><img src="/images/tolkien.png" alt="JRR Tolkien sitting"><p>Here's the deal, <b>I like Tolkien</b>.</p><blockquote>"I am in fact a Hobbit in all but size."\n-- J.R.R. Tolkien</blockquote><h2>Blog posts</h2><ul><li><a href="/blog/glorfindel">Why Glorfindel is More Impressive than Legolas</a></li><li><a href="/blog/tom">Why Tom Bombadil Was a Mistake</a></li><li><a href="/blog/majesty">The Unparalleled Majesty of "The Lord of the Rings"</a></li></ul><h2>Reasons I like Tolkien</h2><ul><li>You can spend years studying the legendarium and still not understand its depths</li><li>It can be enjoyed by children and adults alike</li><li>Disney <i>didn't ruin it</i> (okay, but Amazon might have)</li><li>It created an entirely new genre of fantasy</li></ul></div>"""
        converted_markdown = markdown_to_html_node(markdown)
        converted_html = converted_markdown.to_html()
        self.assertEqual(expected_html, converted_html)
    
if __name__ == '__main__':
    unittest.main()
    
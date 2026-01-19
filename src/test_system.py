import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode
from operations import *
from gencontent import *

class TestHTMLNode(unittest.TestCase):
    

    def test_find_header(self):
        md = """
# Tolkien Fan Club

![JRR Tolkien sitting](/images/tolkien.png)

Here's the deal, **I like Tolkien**.
"""
        header = extract_title(md)
        self.assertEqual(header, "Tolkien Fan Club")
        
    def test_find_header_but_no_header(self):
        md = """
## Tolkien Fan Club

![JRR Tolkien sitting](/images/tolkien.png)

Here's the deal, **I like Tolkien**.
"""
        self.assertRaises(Exception,extract_title,(md))
        
        
    def test_full_md_test(self):
        from_path = "content/index.md"
        template_path = "template.html"
        dest_path = "./"
        source_dir = "./static"
        destination_dir = "./public"

        print(f"Generating page from {from_path} to {dest_path} using {template_path}.")
        input_file = open(from_path)
        md = input_file.read()
        template_file = open(template_path)
        template = template_file.read()
        
        # Convert markdown to HTML
        converted_html = markdown_to_html_node(md)      
        expected_html = """<div><h1>Tolkien Fan Club</h1><img src="/images/tolkien.png" alt="JRR Tolkien sitting"><p>Here\'s the deal, <b>I like Tolkien</b>.</p><blockquote>"I am in fact a Hobbit in all but size."\n-- J.R.R. Tolkien</blockquote><h2>Blog posts</h2><ul><li><a href="/blog/glorfindel">Why Glorfindel is More Impressive than Legolas</a></li><li><a href="/blog/tom">Why Tom Bombadil Was a Mistake</a></li><li><a href="/blog/majesty">The Unparalleled Majesty of "The Lord of the Rings"</a></li></ul><h2>Reasons I like Tolkien</h2><ul><li>You can spend years studying the legendarium and still not understand its depths</li><li>It can be enjoyed by children and adults alike</li><li>Disney <i>didn\'t ruin it</i> (okay, but Amazon might have)</li><li>It created an entirely new genre of fantasy</li></ul><h2>My favorite characters (in order)</h2><ol><li>Gandalf</li><li>Bilbo</li><li>Sam</li><li>Glorfindel</li><li>Galadriel</li><li>Elrond</li><li>Thorin</li><li>Sauron</li><li>Aragorn</li></ol><p>Here\'s what <code>elflang</code> looks like (the perfect coding language):</p><pre><code>func main(){\n    fmt.Println("Aiya, Ambar!")\n}\n</code></pre><p>Want to get in touch? <a href="/contact">Contact me here</a>.</p><p>This site was generated with a custom-built <a href="https://www.boot.dev/courses/build-static-site-generator-python">static site generator</a> from the course on <a href="https://www.boot.dev">Boot.dev</a>.</p></div>"""
        self.assertEqual(converted_html.to_html(),expected_html)
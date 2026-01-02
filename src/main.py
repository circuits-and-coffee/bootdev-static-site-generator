from textnode import TextNode
print("hello world")

def main():
    # The function should create a new TextNode object with some dummy values.
    # Print the object, and make sure it looks like you'd expect. For example, my code printed:
    
    # TextNode(This is some anchor text, link, https://www.boot.dev)
    
    textnode = TextNode("This is some anchor text", "link", "https://www.boot.dev")
    print(textnode)
    return

if __name__ == "__main__":
    main()
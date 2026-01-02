class HTMLNode:
    
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}
        
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        # print(f"Started debugging props_to_html()")
        if self.props is None:
            return ""
        prop_elements = []
        for prop in self.props:
            prop_elements.append(f'{prop}="{self.props[prop]}"')
        # print(f"Debugging props_to_html: {prop_elements}")
        return ' ' + ' '.join(prop_elements)
    
    def __repr__(self):
        # return f"tag = {self.tag}; value = {self.value}; children = {self.children}; props = {self.props}"
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"


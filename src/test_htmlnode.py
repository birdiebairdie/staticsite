import unittest

from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
      node = HTMLNode("p", "This is a text node", [], {"href": "https://www.google.com"})
      node2 = HTMLNode("p", "This is a text node", [], {"href": "https://www.google.com"})
      self.assertEqual(node, node2)

    def test_values(self):
       node = HTMLNode(
          "p",
          "This is a test node",
          [],
          {"href": "https://www.google.com"}
       )
       self.assertEqual(node.tag, "p")
       self.assertEqual(node.value, "This is a test node")
       self.assertEqual(node.children, [])
       self.assertEqual(node.props, {"href": "https://www.google.com"})
          
    def test_props_to_html(self):
       node = HTMLNode(
        "p", 
        "This is a text node", 
        [], 
        {"class": "greeting", "href": "https://www.google.com"}
        )
       self.assertEqual(
          node.props_to_html(),
          ' class="greeting" href="https://www.google.com"'
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
      node = LeafNode(None, "Hello world!")
      self.assertEqual(node.to_html(), "Hello world!")

if __name__ == "__main__":
    unittest.main()
import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
      node = HTMLNode("p", "This is a text node", [], {"href": "https://www.google.com"})
      node2 = HTMLNode("p", "This is a text node", [], {"href": "https://www.google.com"})
      print(f"{node.tag} equals {node2.tag}: {node.tag == node2.tag}")
      print(f"{node.value} equals {node2.value}: {node.value == node2.value}")
      print(f"{node.children} equals {node2.children}: {node.children == node2.children}")
      print(f"{node.props} equals {node2.props}: {node.props == node2.props}")
      self.assertEqual(node, node2)

    def test_tag_not_eq(self):
      node = HTMLNode("p", "This is a text node", [], {"href": "https://www.google.com"})
      node2 = HTMLNode("a", "This is a text node", [], {"href": "https://www.google.com"})
      self.assertNotEqual(node, node2)

    def test_value_not_eq(self):
      node = HTMLNode("p", "This is a text node", [], {"href": "https://www.google.com"})
      node2 = HTMLNode("p", "This is a different text node", [], {"href": "https://www.google.com"})
      self.assertNotEqual(node, node2)
          
    def test_children_not_eq(self):
      node = HTMLNode("p", "This is a text node", [], {"href": "https://www.google.com"})
      node2 = HTMLNode("p", "This is a text node", [HTMLNode(), HTMLNode()], {"href": "https://www.google.com"})
      self.assertNotEqual(node, node2)
          
    def test_props_not_eq(self):
      node = HTMLNode("p", "This is a text node", [], {"href": "https://www.google.com"})
      node2 = HTMLNode("p", "This is a text node", [], {"href": "https://www.github.com"})
      self.assertNotEqual(node, node2)
          
    def test_props_to_html(self):
       node = HTMLNode("p", "This is a text node", [], {"href": "https://www.google.com"})
       print(node.__repr__)

if __name__ == "__main__":
    unittest.main()
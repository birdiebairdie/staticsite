import unittest

from textnode import *

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_diff_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_diff_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_diff_url(self):
        node = TextNode("This is a text node", TextType.BOLD, url="www.beep.com")
        node2 = TextNode("This is a text node", TextType.BOLD, url="www.boop.com")
        self.assertNotEqual(node, node2)

    def test_url_empty_vs_none(self):
        node = TextNode("This is a text node", TextType.BOLD, url="")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)   
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("this is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")

    def test_link(self):
        node = TextNode("this link goes to boop dot com", TextType.LINK, url="boop.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "this link goes to boop dot com")
        self.assertEqual(html_node.props, {"href": "boop.com"})

    def test_image(self):
        node = TextNode("picture of a bumblebee", TextType.IMAGE, url="bumblebeepictures.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "bumblebeepictures.com", "alt": "picture of a bumblebee"})

if __name__ == "__main__":
    unittest.main()
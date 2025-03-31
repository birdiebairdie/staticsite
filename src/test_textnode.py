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

    def test_split_nodes_bold(self):
        nodes = [
            TextNode("This is text with a `code block` word", TextType.TEXT),
            TextNode("This is text with a **bold** word", TextType.TEXT),
            TextNode("This is text with an _italic_ word", TextType.TEXT),
        ]

        code_nodes = split_nodes_delimiter([nodes[0]], "`", TextType.CODE)
        self.assertEqual(code_nodes[0], TextNode("This is text with a ", TextType.TEXT))
        self.assertEqual(code_nodes[1], TextNode("code block", TextType.CODE))
        self.assertEqual(code_nodes[2], TextNode(" word", TextType.TEXT))

        bold_nodes = split_nodes_delimiter([nodes[1]], "**", TextType.BOLD)
        self.assertEqual(bold_nodes[0], TextNode("This is text with a ", TextType.TEXT))
        self.assertEqual(bold_nodes[1], TextNode("bold", TextType.BOLD))
        self.assertEqual(bold_nodes[2], TextNode(" word", TextType.TEXT))


if __name__ == "__main__":
    unittest.main()
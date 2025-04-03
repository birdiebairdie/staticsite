import unittest

from textnode import TextNode, TextType
from inline_markdown import (
  split_nodes_delimiter,
  extract_markdown_links,
  extract_markdown_images,
  split_nodes_image,
  split_nodes_link,
  text_to_textnodes,
)

class TestInlineMarkdown(unittest.TestCase):
  def test_split_nodes_bold(self):
    nodes = [
      TextNode("This is text with a `code block` word", TextType.TEXT),
      TextNode("This is text with a **bold** word", TextType.TEXT),
      TextNode("This is text with an _italic_ word", TextType.TEXT),
    ]

    code_node = split_nodes_delimiter([nodes[0]], "`", TextType.CODE)
    self.assertEqual(code_node[0], TextNode("This is text with a ", TextType.TEXT))
    self.assertEqual(code_node[1], TextNode("code block", TextType.CODE))
    self.assertEqual(code_node[2], TextNode(" word", TextType.TEXT))

    bold_nodes = split_nodes_delimiter([nodes[1]], "**", TextType.BOLD)
    self.assertEqual(bold_nodes[0], TextNode("This is text with a ", TextType.TEXT))
    self.assertEqual(bold_nodes[1], TextNode("bold", TextType.BOLD))
    self.assertEqual(bold_nodes[2], TextNode(" word", TextType.TEXT))

    
  
  def test_extract_markdown_images(self):
    matches = extract_markdown_images(
      "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    )
    self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

  def test_extract_markdown_links(self):
    matches = extract_markdown_links(
      "This is text with a [link](https://www.boop.com) and [a different link](beep.com)"
    )
    self.assertListEqual([("link", "https://www.boop.com"), ("a different link", "beep.com")], matches)

  def test_split_images(self):
    node = TextNode(
      "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
      TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
      [
        TextNode("This is text with an ", TextType.TEXT),
        TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        TextNode(" and another ", TextType.TEXT),
        TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
      ],
      new_nodes,
    )

    def test_split_links(self):
      node = TextNode(
        "This is text with a [link](https://www.boop.com) and another [second link](beep.com)",
        TextType.TEXT,
      )
      new_nodes = split_nodes_link([node])
      self.assertListEqual(
        [
          TextNode("This is text with an ", TextType.TEXT),
          TextNode("link", TextType.LINK, "https://www.boop.com"),
          TextNode(" and another ", TextType.TEXT),
          TextNode("second link", TextType.LINK, "beep.com"),
        ],
        new_nodes,
      )

    def test_text_to_textnodes(self):
      text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

      split_text = text_to_textnodes(text)
      self.assertListEqual(
        [
          TextNode("This is ", TextType.TEXT),
          TextNode("text", TextType.BOLD),
          TextNode(" with an ", TextType.TEXT),
          TextNode("italic", TextType.ITALIC),
          TextNode(" word and a ", TextType.TEXT),
          TextNode("code block", TextType.CODE),
          TextNode(" and an ", TextType.TEXT),
          TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
          TextNode(" and a ", TextType.TEXT),
          TextNode("link", TextType.LINK, "https://boot.dev"),
        ],
        split_text
      )
if __name__ == "__main__":
    unittest.main()
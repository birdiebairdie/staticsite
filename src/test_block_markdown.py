import unittest

from block_markdown import (
  markdown_to_blocks,
  block_to_block_type, 
  markdown_to_html_node,
  BlockType
)


class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items"""

        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type(self):
        md_heading = "### This is a heading"

        md_code = """```
This is a code block
with several lines
```
"""
        
        md_quote = """>This is a properly
>formatted
>block quote."""

        md_ulist = """- This is a properly
- formatted
- unordered
- list.
"""

        md_ulist_wrong = """- This is an
-improperly
- formatted
-unordered list.
"""

        md_olist = """1. This is a 
2. properly formatted
3. ordered list
"""

        md_paragraph = """
This is a standard paragraph
with multiple lines
separated by line breaks
"""

        heading_type = block_to_block_type(md_heading)
        code_type = block_to_block_type(md_code)
        quote_type = block_to_block_type(md_quote)
        ulist_type = block_to_block_type(md_ulist)
        ulist_wrong_type = block_to_block_type(md_ulist_wrong)
        olist_type = block_to_block_type(md_olist)
        paragraph_type = block_to_block_type(md_paragraph)

        self.assertEqual(heading_type, BlockType.HEADING)
        self.assertEqual(code_type, BlockType.CODE)
        self.assertEqual(quote_type, BlockType.QUOTE)
        self.assertEqual(ulist_type, BlockType.ULIST)
        self.assertEqual(ulist_wrong_type, BlockType.PARAGRAPH)
        self.assertEqual(olist_type, BlockType.OLIST)
        self.assertEqual(paragraph_type, BlockType.PARAGRAPH)

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

if __name__ == "__main__":
    unittest.main()
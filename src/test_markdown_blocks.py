import unittest

from markdown_blocks import BlockType
from markdown_blocks import (
    markdown_to_blocks,
    block_to_block_type,
    markdown_to_html_node,
    process_paragraph,
    process_heading,
    process_code,
    process_quote,
    process_unordered_list,
    process_ordered_list
)


class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


    def test_paragraph(self):
        md = "This is a paragraph"
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_heading(self):
        md = "## This is a heading"
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.HEADING)

    def test_code(self):
        md = "```\nSome code\n```"
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.CODE)

    def test_quote(self):
        md = ">This is a quote"
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.QUOTE)

    def test_unordered_list_one_line(self):
        md = "- This is a list"
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.UNORDERED_LIST)

    def test_ordered_list_one_line(self):
        md = "1. This is an ordered list"
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.ORDERED_LIST)

    def test_quote_multiline(self):
        md = ">Line 1\n>Line 2\n>Line 3"
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.QUOTE)

    def test_unordered_list_multiline(self):
        md = "- Item 1\n- Item 2\n- Item 3"
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.UNORDERED_LIST)

    def test_ordered_list_multiline(self):
        md = "1. Item 1\n2. Item 2\n3. Item 3"
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.ORDERED_LIST)


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

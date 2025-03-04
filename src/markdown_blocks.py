from enum import Enum

from htmlnode import ParentNode
from inline_markdown import text_to_children
from textnode import TextNode, text_node_to_html_node, TextType

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


def block_to_block_type(md_block):
    if md_block.startswith("#"):
        heading_parts = md_block.split(" ", 1)
        if len(heading_parts) > 1 and 1 <= len(heading_parts[0]) <= 6 and all(char == "#" for char in heading_parts[0]):
            return BlockType.HEADING
        
    if md_block.startswith("```") and md_block.endswith("```") and len(md_block) >= 6:
        return BlockType.CODE
        
    if md_block.startswith(">"):
        lines = md_block.splitlines()
        if all(line.startswith(">") for line in lines):
            return BlockType.QUOTE
        
    if md_block.startswith("- "):
        lines = md_block.splitlines()
        if all(line.startswith("- ") for line in lines):
            return BlockType.UNORDERED_LIST
        
    if md_block.startswith("1. "):
        lines = md_block.splitlines()
        expected_number = 1
        for line in lines:
            expected_prefix = f"{expected_number}. "
            if not line.startswith(expected_prefix):
                break
            expected_number += 1
        else:
            return BlockType.ORDERED_LIST
        
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    md_blocks = markdown_to_blocks(markdown)
    html_blocks = []
    for block in md_blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            html_blocks.append(process_paragraph(block))
        elif block_type == BlockType.HEADING:
            html_blocks.append(process_heading(block))
        elif block_type == BlockType.CODE:
            html_blocks.append(process_code(block))
        elif block_type == BlockType.QUOTE:
            html_blocks.append(process_quote(block))
        elif block_type == BlockType.UNORDERED_LIST:
            html_blocks.append(process_unordered_list(block))
        elif block_type == BlockType.ORDERED_LIST:
            html_blocks.append(process_ordered_list(block))
    return ParentNode("div", html_blocks)

def process_paragraph(block):
    children = text_to_children(block)
    return ParentNode("p", children)

def process_heading(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    text = block[level+1:]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def process_code(block):
    code_content = block[3:-3].strip()
    code_node = text_node_to_html_node(TextNode(code_content, TextType.CODE))
    return ParentNode("pre", [code_node])

def process_quote(block):
    lines = block.split("\n")
    quote_content = ""
    for line in lines:
        if line.startswith("> "):
            quote_content += line[2:] + "\n"
        elif line.strip() == "":
            quote_content += "\n"
        else:
            quote_content += line + "\n"
    quote_content = quote_content.rstrip()
    return ParentNode("blockquote", text_to_children(quote_content))

def process_unordered_list(block):
    lines = block.split("\n")
    list_items = []
    for line in lines:
        if line.startswith("- "):
            item_content = line[2:].strip()
            list_items.append(ParentNode("li", text_to_children(item_content)))
    return ParentNode("ul", list_items)

def process_ordered_list(block):
    lines = block.split("\n")
    list_items = []
    for line in lines:
        if line and line[0].isdigit() and ". " in line:
            period_pos = line.find(". ")
            if period_pos != -1:
                item_content = line[period_pos + 2:].strip()
                list_items.append(ParentNode("li", text_to_children(item_content)))
    return ParentNode("ol", list_items)
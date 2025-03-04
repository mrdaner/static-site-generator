from enum import Enum


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
import re

from textnode import TextNode, TextType, text_node_to_html_node


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        images = extract_markdown_images(old_node.text)

        if not images:
            new_nodes.append(old_node)
            continue

        split_text = old_node.text
        for image_alt, image_url in images:
            parts = split_text.split(f"![{image_alt}]({image_url})", 1)

            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))

            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))

            split_text = parts[1] if len(parts) > 1 else ""
        
        if split_text:
            new_nodes.append(TextNode(split_text, TextType.TEXT))
        
    return new_nodes            


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        links = extract_markdown_links(old_node.text)

        if not links:
            new_nodes.append(old_node)
            continue

        split_text = old_node.text
        for link_alt, link_url in links:
            parts = split_text.split(f"[{link_alt}]({link_url})", 1)

            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))

            new_nodes.append(TextNode(link_alt, TextType.LINK, link_url))

            split_text = parts[1] if len(parts) > 1 else ""
        
        if split_text:
            new_nodes.append(TextNode(split_text, TextType.TEXT))
        
    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]

    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    delimiter_types=[
        ("**", TextType.BOLD),
        ("_", TextType.ITALIC),
        ("`", TextType.CODE)
    ]
    
    for delimiter, text_type in delimiter_types:
        nodes = split_nodes_delimiter(nodes, delimiter, text_type)
    
    return nodes



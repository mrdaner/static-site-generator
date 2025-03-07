import os
from markdown_blocks import markdown_to_html_node


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    from_file = open(from_path, "r")
    markdown_content = from_file.read()
    from_file.close()

    template_file = open(template_path, "r")
    template_content = template_file.read()
    template_file.close()

    html_content = markdown_to_html_node(markdown_content).to_html()

    markdown_title = extract_title(markdown_content)
    final_html = template_content.replace("{{ Title }}", markdown_title)
    final_html = final_html.replace("{{ Content }}", html_content)

    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)
    dest_file = open(dest_path, "w")
    dest_file.write(final_html)
    dest_file.close()

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith("# "):
            return stripped_line[2:].strip()
    raise Exception("invalid header")
import os
import shutil

from textnode import TextNode, TextType


def main():
    node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print(node)
    copy_static_directory("static", "public")

def copy_static_directory(source_dir, dest_dir):
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    os.mkdir(dest_dir)
    
    for item in os.listdir(source_dir):
        source_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)
        if os.path.isfile(source_path):
            shutil.copy(source_path, dest_path)
            print(f"Copied file: {source_path} to {dest_path}")
        else:
            os.mkdir(dest_path)
            print(f"Created directory: {dest_path}")
            copy_static_directory(source_path, dest_path)
            print(f"Finished copying directory: {source_path}")


main()
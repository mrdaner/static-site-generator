import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_props_to_html(self):
        props = {"href": "https://www.google.com", "target": "_blank"}
        node = HTMLNode(props=props)
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_repr(self):
        node = HTMLNode(tag="a", value="Click me", props={"href": "https://example.com"})
        repr_string = repr(node)
        # Check that the representation contains key information
        self.assertIn("a", repr_string)  
        self.assertIn("Click me", repr_string)
        self.assertIn("href", repr_string)



if __name__ == "__main__":
    unittest.main()
import unittest
from gencontent import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_valid_h1(self):
        markdown = "# Hello, world!"
        self.assertEqual(extract_title(markdown), "Hello, world!")

    def test_multiple_lines(self):
        markdown = "### Subheading\n# Main Title\nSome text"
        self.assertEqual(extract_title(markdown),"Main Title")

    def test_no_h1_header(self):
        markdown = "Some random\n## Subheading\nContent"
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "invalid header")

    def test_empty_markdown(self):
        markdown = ""
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "invalid header")

    def test_leading_and_trailing_whitespace(self):
        markdown = "       \n   #    Spaced Out Title   \n   "
        self.assertEqual(extract_title(markdown), "Spaced Out Title")


if __name__ == "__main__":
    unittest.main()
import unittest
from generate_page import extract_title



class TestTextNode(unittest.TestCase):

    def test_extract_title(self):
        md = "# Header 1"
        result = extract_title(md)
        expected = "Header 1"
        self.assertEqual(result, expected)

    def test_multiline_title(self):
        md = """
First line is not

# Header
        """
        result = extract_title(md)
        expected = "Header"
        self.assertEqual(result, expected)
        
    def test_multiple_h1(self):
        # Should get first header
        md = """
# Header 1

# Header 2
        """
        result = extract_title(md)
        expected = "Header 1"
        self.assertEqual(result, expected)
        
    def test_extract_title_errors(self):

        md = "## Header 2"

        with self.assertRaises(ValueError):
            print(extract_title(md))
            
    def test_hastag_error(self):
        md = "#Bad Header"
        
        with self.assertRaises(ValueError):
            print(extract_title(md))

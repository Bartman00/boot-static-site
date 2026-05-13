import unittest

from file_utilities import get_text_file


class TestFileUtilities(unittest.TestCase):

    def test_read_file(self):
        filepath = "template.html"

        result = get_text_file(filepath)
        expected = """<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{{ Title }}</title>
    <link href="/index.css" rel="stylesheet" />
  </head>

  <body>
    <article>{{ Content }}</article>
  </body>
</html>"""
        self.assertEqual(result, expected)
        
    def test_read_errors(self):
        filepath = "madup.html"

        with self.assertRaises(FileNotFoundError):
            print(get_text_file(filepath))
            
    def test_read_file_error(self):
        filepath = "src/"


        with self.assertRaises(ValueError):
            print(get_text_file(filepath))

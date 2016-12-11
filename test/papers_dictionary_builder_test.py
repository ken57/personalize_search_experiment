# encoding: utf-8
import unittest
from authors_network.papers_dictionary_builder import PapersDictionaryBuilder

class TestPapersDictionaryBuilder(unittest.TestCase):
    def test_build(self):
        builder = PapersDictionaryBuilder()
        papers = builder.build('resource/test.txt')
        self.assertEqual(papers['0'].title, 'hogehogepaper')
        self.assertEqual(papers['0'].authors, ['author1', 'author2'])
        self.assertEqual(papers['0'].year, '2006')
        self.assertEqual(papers['0'].venue, '')
        self.assertEqual(papers['0'].abstract, 'abst')
        self.assertEqual(papers['0'].references, [])

        self.assertEqual(papers['1'].title, 'paper2')
        self.assertEqual(papers['1'].authors, ['author3'])
        self.assertEqual(papers['1'].year, '2003')
        self.assertEqual(papers['1'].venue, 'computer')
        self.assertEqual(papers['1'].abstract, '')
        self.assertEqual(papers['1'].references, ['0', '2'])

if __name__ == '__main__':
    unittest.main()

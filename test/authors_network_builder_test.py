# encoding: utf-8
import unittest
from authors_network.authors_network_builder import AuthorsNetworkBuilder
from authors_network.papers_dictionary_builder import PapersDictionaryBuilder

class TestAuthorsNetworkBuilder(unittest.TestCase):
    def test_build(self):
        builder = AuthorsNetworkBuilder()
        papersDictionaryBuilder = PapersDictionaryBuilder()
        papers = papersDictionaryBuilder.build('resource/test.txt')
        authors = builder.build(papers)
        self.assertEqual(set(authors['author1']), set(['author2', 'author4']))
        self.assertEqual(authors['author2'], ['author1'])
        self.assertEqual(set(authors['author3']), set(['author1', 'author2', 'author4', 'author5', 'author6']))
        self.assertEqual(authors['author4'], ['author1'])

if __name__ == '__main__':
    unittest.main()

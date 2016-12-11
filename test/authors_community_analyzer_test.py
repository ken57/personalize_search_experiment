# encoding: utf-8
import unittest
from collections import Counter
from authors_network.authors_network_builder import AuthorsNetworkBuilder
from authors_network.authors_community_analyzer import AuthorsCommunityAnalyzer
from authors_network.papers_dictionary_builder import PapersDictionaryBuilder

class TestAuthorsCommunityAnalyzer(unittest.TestCase):
    def test_analyzeAuthorsInterest(self):
        analyzer = AuthorsCommunityAnalyzer()
        papersDictionaryBuilder = PapersDictionaryBuilder()
        papers = papersDictionaryBuilder.build('resource/test.txt')
        ai = analyzer.analyzeAuthorsInterest(papers)
        self.assertEqual(ai['author1'], Counter({u'paper3': 1, u'hogehogepaper': 1}))
        self.assertEqual(ai['author3'], Counter({u'fuga': 2, u'computer': 1, u'hoge': 1, u'paper4': 1, u'paper2': 1, u'paper3': 1}))

    def test_analyze(self):
        builder = AuthorsNetworkBuilder()
        analyzer = AuthorsCommunityAnalyzer()
        papersDictionaryBuilder = PapersDictionaryBuilder()
        papers = papersDictionaryBuilder.build('resource/test.txt')
        authors = builder.build(papers)
        analyzer.analyze(authors, papers)
        expectedJson = '{"directed": false, "graph": {}, "nodes": [{"id": 0, "interest": ["paper3", "hogehogepaper"], "size": 3}, {"id": 1, "interest": ["fuga", "hoge", "paper4", "computer", "paper2"], "size": 3}], "links": [{"source": 0, "target": 0, "weight": 4}, {"source": 0, "target": 1, "weight": 3}, {"source": 1, "target": 1, "weight": 4}], "multigraph": false}'

        self.assertEqual(analyzer.analyze(authors, papers), expectedJson)
        print("cmp")

if __name__ == '__main__':
    unittest.main()

# encoding: utf-8
import json
import sys
import os
from networkx.readwrite import json_graph

from authors_network.authors_network_builder import AuthorsNetworkBuilder
from authors_network.papers_dictionary_builder import PapersDictionaryBuilder
from authors_network.authors_community_analyzer import AuthorsCommunityAnalyzer

def main(papers_filename, output_dirname):
    builder = AuthorsNetworkBuilder()
    analyzer = AuthorsCommunityAnalyzer()
    papersDictionaryBuilder = PapersDictionaryBuilder()
    papers = papersDictionaryBuilder.build(papers_filename)
    print('reading papers is complete.')
    authors = builder.build(papers)
    print('building authors network is complete.')
    result = analyzer.analyze(authors, papers)
    print('analyzing networks complete.')
    data = json_graph.node_link_data(result.induced_graph)
    s = json.dumps(data, ensure_ascii=False)

    if not os.path.isdir(output_dirname):
        os.makedirs(output_dirname)

    with open(output_dirname + '/network.json', 'w', encoding='UTF-8') as f:
        f.write(s)
    with open(output_dirname + '/authors.txt', 'w', encoding='UTF-8') as f:
        for author, community in result.authors_community.items():
            f.write(author + " " + str(community) + "\n")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("usage: python analyzer_runner.py [papers filename] [output dirname]")
    main(sys.argv[1], sys.argv[2])

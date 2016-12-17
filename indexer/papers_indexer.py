# encoding: utf-8
import sys
sys.path.append('../')

import codecs
import json
import urllib.request
from authors_network.papers_dictionary_builder import PapersDictionaryBuilder

def main(papers_filename, authors_filename,url ):
    u"""論文をインデクシングするスクリプトです."""

    author_classes ={}
    file = codecs.open(authors_filename, 'r', 'utf-8')
    for line in file:
        words = line.rstrip().split(' ')
        if len(words) > 1:
            author = words[0]
            cluster = words[1]
            author_classes[author] = cluster

    papersDictionaryBuilder = PapersDictionaryBuilder()
    papers = papersDictionaryBuilder.build(papers_filename)
    print(len(papers))

    data = ""
    count = 0
    for index, paper in papers.items():
        if len(paper.authors) > 0:
            author_class = "null"
            if paper.authors[0] in author_classes:
                author_class = "\"" + str(author_classes[paper.authors[0]]) + "\""

            data += "{\"create\" : {\"_id\" : " + json.dumps(str(paper.index)) + ", \"_type\" : \"paper\", \"_index\" : \"papers\"}}\n"
            data += "{\"title\": " + json.dumps(paper.title) + ", \"first_author\": " + json.dumps(paper.authors[0]) + ", \"abstract\": "\
                + json.dumps(paper.abstract) + ", \"venue\": " + json.dumps(paper.venue) + ", \"year\": "\
                + json.dumps(paper.year) + ", \"authors\": " + json.dumps(" ".join(paper.authors)) + ", \"references\": "\
                + json.dumps(" ".join(paper.references)) + ", \"class\": " + author_class + "}\n"
            if count > 1000:
                req = urllib.request.Request(url + '/_bulk', data.encode('utf-8'))
                urllib.request.urlopen(req)
                data = ""
                count = 0
                print(data)

            count = count + 1
            print(count)
    print(data)
    req = urllib.request.Request(url, data.encode('utf-8'))
    urllib.request.urlopen(req)

if __name__ == '__main__':
    argv = sys.argv
    if len(sys.argv) < 3:
        print("usage: python papers_indexer.py [papers file] [authors file] [elasticsearch host]")
    main(sys.argv[0], sys.argv[1], sys.argv[2])

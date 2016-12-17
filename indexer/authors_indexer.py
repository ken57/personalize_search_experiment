# encoding: utf-8
import codecs
import json
import urllib.request
import sys

def main(filename, url):
    u"""著者とクラスタの関係をインデクシングするスクリプトです."""

    author_class ={}
    file = codecs.open(filename, 'r', 'utf-8')
    for line in file:
        words = line.rstrip().split(' ')
        if len(words) > 1:
            author = words[0]
            cluster = words[1]
            author_class[author] = cluster

    data = ""
    count = 0
    for k, v in author_class.items():
        data += "{\"create\" : {\"_id\" : " + json.dumps(k) + ", \"_type\" : \"author\", \"_index\" : \"authors\"}}\n"
        data += "{\"class\": \"" + v + "\"}\n"
        if count > 1000:
            print(data)
            req = urllib.request.Request(url + '/_bulk', data.encode('utf-8'))
            urllib.request.urlopen(req)
            data = ""
            count = 0

        count = count + 1
        print(count)
    print(data)
    if data:
        req = urllib.request.Request(url, data.encode('utf-8'))
        urllib.request.urlopen(req)

if __name__ == '__main__':
    argv = sys.argv
    if len(sys.argv) < 2:
        print("usage: python authors_indexer.py [authors file] [elasticsearch host]")
    main(sys.argv[0], sys.argv[1])

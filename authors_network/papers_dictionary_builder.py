# encoding: utf-8
import codecs
from authors_network.paper import Paper

class PapersDictionaryBuilder:
    def build(self, filename):
        u"""論文データを読み込んで { 論文番号 : Paper(論文情報) } を返す"""
        papers = {}
        file = codecs.open(filename, 'r', 'utf-8')
        line = file.readline()  # 最初の行は総論文数
        while line:
            paperLines = []
            while line[:1] == '#':
                paperLines.append(line.strip())
                line = file.readline()
            paper = self.__buildPaper(paperLines)
            papers[paper.index] = paper
            line = file.readline()
        return papers

    def __buildPaper(self, lines):
        title = ''
        authors = []
        year = ''
        venue = ''
        index = ''
        references = []
        abstract = ''

        for line in lines:
            head = line[:2]
            if head == '#*':
                title = line[2:]
            elif head == '#@':
                authors = [author.replace(' ', '_') for author in line[2:].split(',')]
            elif head == '#i':
                index = line[6:]
            elif head == '#t':
                year = line[2:]
            elif head == '#c':
                venue = line[2:]
            elif head == '#%':
                references.append(line[2:])
            elif head == '#!':
                abstract = line[2:]

        return Paper(title, authors, year, venue, index, references, abstract)

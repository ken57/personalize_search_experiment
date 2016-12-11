# encoding: utf-8

class AuthorsNetworkBuilder:
    def build(self, papers):
        authors_network = {}
        for index, paper in papers.items():
            # 共著関係から著者間のリンクを作る
            for author in paper.authors:
                if author in authors_network:
                    authors_network[author] = list(set(authors_network[author] + paper.authors))
                else:
                    authors_network[author] = paper.authors

            # 引用関係から著者間のリンクを作る
            referedAuthors = self.__getReferedAuthors(papers, paper.references)
            for author in paper.authors:
                if author in authors_network:
                    authors_network[author] = list(referedAuthors.union(set(authors_network[author])))
                else:
                    authors_network[author] = list(referedAuthors)

        # 自分へのリンクを切る
        for author in authors_network.keys():
            authors_network[author] = filter(lambda a: a != author, authors_network[author])

        return authors_network
        """著者同士のネットワークを返す"""

    def __getReferedAuthors(self, papers, references):
        referedAuthors = set()
        for referedPaper in references:
            if referedPaper in papers:
                for referedAuthor in papers[referedPaper].authors:
                    referedAuthors.add(referedAuthor)
            #else:
                #print("いねえ")
        return referedAuthors

# encoding: utf-8
import math
import collections
import re
from collections import Counter
from nltk.corpus import stopwords

class CommunityInterestAnalyzer:
    u"""クラスタリングしたコミュニティごとの興味分野をTFIDFで求めるクラス"""
    def __init__(self):
        self.__stopwords_set = set(stopwords.words('english'))

    def analyze(self, induced_graph, clusterids_nodes_dict, papers):
        u""" クラスタリングしたコミュニティごとの興味分野をTFIDFで求めmます
        induced_graph: グラフクラスタリングの結果により縮約されたグラフ
        cluesterids_nodes_dict: { クラスタ番号 , [クラスタに含まれるnodes...] }の辞書
        papers: 論文
        """
        induced_graph_with_interest = induced_graph.copy()
        clusters_interest = self.analyzeClustersInterest(clusterids_nodes_dict, papers)
        for v in induced_graph_with_interest.nodes():
            induced_graph_with_interest.node[v]['interest'] = clusters_interest[v]
            induced_graph_with_interest.node[v]['size'] = len(clusterids_nodes_dict[v])

        return induced_graph_with_interest
        u"""興味分野の単語を追加されたinduced_graph"""


    def getWordsByRemovingStopWords(self, interest, words_number = 5):
        u"""ストップワードを除いた単語リストを頻度順で返す"""
        return list(set(map(lambda wc: wc[0],interest.most_common())) - self.__stopwords_set)[:words_number]

    def analyzeAuthorsInterest(self, papers):
        u"""著者が書いた論文のタイトルの単語をカウントし、著者の興味分野を求める"""
        authors_interest_counter = {}
        for index, paper in papers.items():

            words = re.sub(re.compile("[!-/:-@[-`{-~]"), '', paper.title).lower().split()
            for author in paper.authors:
                if author in authors_interest_counter:
                    authors_interest_counter[author] = authors_interest_counter[author] + Counter(words)
                else:
                    authors_interest_counter[author] = Counter(words)
        return authors_interest_counter
        u""" return: { 著者名 : 単語のCounter}"""

    def analyzeClustersInterest(self, clusters, papers):
        u""" クラスタに含まれる著者が書いた論文のタイトルの単語をカウントし、クラスタの興味分野を求める(TF-IDFを使用)"""
        authors_interest = self.analyzeAuthorsInterest(papers)
        clusters_interest_counter = {}
        temp_idf = collections.defaultdict(set)
        for clusterId, cluster in clusters.items():
            counter = Counter()
            for author in clusters[clusterId]:
                counter = counter + authors_interest[author]
                clusters_interest_counter[clusterId] = counter
            for word in list(counter):
                temp_idf[word].add(clusterId)

        # idfの計算
        idf = {}
        cluster_num = len(clusters.keys())
        for word in temp_idf.keys():
            idf[word] = math.log(cluster_num / len(temp_idf[word])) + 1

        # tfidfの計算
        clusters_interest_bytfidf = collections.defaultdict(list)
        for clusterId, counter in clusters_interest_counter.items():
            wordSum = sum(counter.values())
            wordScores = {}
            for word, num in counter.items():
                wordScores[word] = idf[word] * num / wordSum
            # ストップワードを削りながらtfidf値が高い順に5つの単語を取得
            clusters_interest_bytfidf[clusterId] = sorted([x for x in wordScores.items() if not x[0] in self.__stopwords_set], key=lambda x:x[1], reverse=True)[:5]
        return clusters_interest_bytfidf
        u""" return: { クラスタ番号 : 単語のCounter}"""


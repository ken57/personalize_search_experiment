# encoding: utf-8
import community
import networkx as nx
import collections

from authors_network.community_interest_analyzer import CommunityInterestAnalyzer

class AuthorsCommunityAnalyzingResult:
    def __init__(self, induced_graph, authors_community, ):
        # グラフクラスタリングにより縮約されたグラフ
        self.induced_graph = induced_graph
        # [著者：コミュニティ番号]の辞書
        self.authors_community = authors_community

class AuthorsCommunityAnalyzer:
    u"""論文著者のネットワークに対してグラフクラスタリングを行うクラス"""

    def __init__(self, valid_minimum_subgraph_size = 50):
        # 下記の人数以下で構成されるサブグラフは無視する
        self.__valid_minimum_subgraph_size = valid_minimum_subgraph_size

    def analyze(self, authors_network, papers):
        u"""論文著者のネットワークに対してグラフクラスタリングを行う。おまけでクラスタの興味分野の単語も求める。"""

        # クラスタリングする
        graph = nx.DiGraph(authors_network)
        connected_graph = self.getConnectedGraph(graph)
        nodes_clusterids_dict = community.best_partition(connected_graph.to_undirected())

        clusterids_nodes_dict = self.getClusters(nodes_clusterids_dict)

        # クラスタの興味分野を求める
        community_interest_analyzer = CommunityInterestAnalyzer()
        induced_graph = community_interest_analyzer.analyze(
            community.induced_graph(nodes_clusterids_dict, connected_graph),
            clusterids_nodes_dict, papers)

        return AuthorsCommunityAnalyzingResult(induced_graph, nodes_clusterids_dict)

    def getConnectedGraph(self, graph):
        u"""非連続で細かすぎるサブグラフを構成するノードを除去したグラフを返す"""
        connected_graphs = sorted(nx.weakly_connected_component_subgraphs(graph), key=len, reverse=True)
        connected_nodes = []
        for g in connected_graphs:
            if len(g.nodes()) < self.__valid_minimum_subgraph_size:
                break
            for n in g.nodes():
                connected_nodes.append(n)
        return graph.subgraph(connected_nodes)


    def getClusters(self, partition):
        u"""{ノード : クラスタID}を{クラスタID : ノードs}にする"""
        partition_inv = collections.defaultdict(list)
        for k, v in partition.items():
            partition_inv[v].append(k)
        return partition_inv

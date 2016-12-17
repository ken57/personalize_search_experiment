# 概要

下記のqiita記事を書くために作成した実験用のスクリプトです。 
「グラフクラスタリングを使用したパーソナライズ検索について」
 http://qiita.com/k_ishi/items/8c629ccc0747078eb01a


# 使い方
## 1. 論文引用関係のファイルのダウンロード
    curl -L -O http://aminer.org/lab-datasets/citation/citation-network1.zip
    unzip citation-network1.zip

## 2. 著者関係のグラフクラスタリングを行う
    python analyzer_runner.py [1で取得したファイルを指定] [データ出力先のディレクトリを指定]

3時間くらいかかります。
完了すると、[データ出力先のディレクトリを指定]の配下に下記のファイルが生成されます。

・network.json： グラフクラスタリングの結果をもとに縮約されたグラフのjsonファイルです。
　　　　　　　　　記事中の図を出力するために使用しています。

・authors.txt：　グラフクラスタリングの結果のファイルです。[著者名:クラスタ番号]の形式になっています。

## 3. ESへのインデクシング

### 3.1. authorsインデックス
    python indexer/authors_indexer.py [2で生成したauthors.txt] [ESのホスト(例 http://localhost:9200)]

### 3.2. papersインデックス
    python indexer/papers_indexer.py [1で取得したファイル名] [2で生成したauthors.txt] [ESのホスト(例 http://localhost:9200)]

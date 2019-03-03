# 某アイカツ！ランキングを取得して Mastodon に投げ込む

## 使い方

Mastodon に投げ込む為に client id, client secret と access token を取得します。  
参考: https://qiita.com/itsumonotakumi/items/1f9273a07f1f7189921f

aikatsu_ranking.py と同じ場所に mastodon.ini を置き、取得した値を設定して下さい。

## 何をしているのか

ランキングにある「もっと読む」をタッチしたときに Ajax で取ってくる HTML のテーブルデータをパースしています。

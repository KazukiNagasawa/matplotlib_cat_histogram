# matplotlib_cat_histogram
Matplotlibを用いて猫画像とそのヒストグラムを同時に表示するサンプル。gridspec習作。

## 環境
- Python 3.5
    - matplotlib
    - numpy
    - opencv-python
    - requests
        - 猫画像取得に使用

## 実行
```
$ python3 execute.py
```
実行すると、
まず [Oxford Pet Dataset](http://www.robots.ox.ac.uk/~vgg/data/pets) からデータ、アノテーションファイルを取得し、/tmp/cat_data に配置します。( 配置場所変更する場合はソースコード編集。)  
  
その後、ウィンドウが表示され、猫画像と RGB のヒストグラムが表示されます。  
  
表示は2秒ごとに更新されます。



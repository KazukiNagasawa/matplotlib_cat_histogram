# -*- coding: utf-8 -*-


import glob
import os
import random
import shutil
import tarfile
import xml.etree.ElementTree as ET

import requests

from PIL import Image, ImageDraw


'''
猫顔取得 (Oxford 猫犬データセットより)
'''


### ダウンロード URL
# 画像
IMAGES_URL = "http://www.robots.ox.ac.uk/%7Evgg/data/pets/data/images.tar.gz"
# アノテーション
ANNOTATIONS_URL = "http://www.robots.ox.ac.uk/%7Evgg/data/pets/data/annotations.tar.gz"


class Cats(object) :

    def __init__(self, data_dir = "/tmp/cat_faces") :

        if not os.path.exists(data_dir) :
            os.makedirs(data_dir)

        ### Download files
        self.images_dir = self._download_file(IMAGES_URL, data_dir)
        self.annotations_dir = self._download_file(ANNOTATIONS_URL, data_dir)

        ### Get data
        self.cat_data = self._load_cat_data(self.annotations_dir)
        self.len_cats = len(self.cat_data)


    def get_cat_path(self, idx) :
        ''' idx 番目の猫画像パスを取得 '''
        assert idx < self.len_cats

        cat = self.cat_data[idx]['name']
        return os.path.join(self.images_dir, "{}.jpg".format(cat))


    def get_cat_face(self, idx) :
        ''' idx 番目の猫顔rectを取得 '''
        assert idx < self.len_cats

        cat = self.cat_data[idx]['name']
        xml_path = os.path.join(self.annotations_dir, "xmls", "{}.xml".format(cat))
        return self._get_rect_from_xml(xml_path)


    def __len__(self) :
        ''' 猫データセット数 '''
        return self.len_cats


    def _download_file(self, url, output_dir) :
        ''' output_dir 配下に url のファイルをダウンロードする '''
        name = os.path.basename(url)
        output_path = "{dir}/{name}".format(dir = output_dir, name = name)
        if not os.path.exists(output_path) :
            print("Download from '{url}'".format(url = url))
            res = requests.get(url, stream = True)
            with open(output_path, 'wb') as f :
                shutil.copyfileobj(res.raw, f)

        extracted_path = "{dir}/{name}".format(dir = output_dir, name = name.split('.')[0])
        if not os.path.exists(extracted_path) :
            print("Extract file '{name}'".format(name = name))
            self._extract(output_path, output_dir)

        return extracted_path


    def _extract(self, tar_path, output_path) :
        ''' tar.gz 展開 '''
        arc_file = tarfile.open(tar_path)
        arc_file.extractall(output_path)
        arc_file.close()


    def _load_cat_data(self, annotations_dir) :
        ''' 猫画像データリスト読み込み '''

        annotations_list = os.path.join(annotations_dir, "list.txt")

        data = []
        with open(annotations_list, 'r') as f :
            for line in f.readlines() :
                line = line.strip()
                if line[0] == "#" :  # コメント行
                    continue
                datum = line.split(" ")
                if len(datum) < 4 : # データ不足行
                    continue
                if datum[2] == "1" : # 猫データのみ取得
                    data.append({'name': datum[0], 'label': int(datum[3])})
        return data



    def _get_rect_from_xml(self, path) :
        ''' XMLファイルから rect 情報を取得 '''
        if not os.path.exists(path) :
            return None
        tree = ET.parse(path)
        root = tree.getroot()
        result = []
        for elm_name in ["xmin", "ymin", "xmax", "ymax"] :
            text = self._get_text(root, "object/bndbox/" + elm_name)
            if text is None :
                return None
            result.append(int(text))
        return result



    def _get_text(self, root, elm_name) :
        ''' XML root から指定した名前空間内の text を取得 '''
        elm = root.find(elm_name)
        if elm is None :
            return None
        return elm.text



if __name__ == '__main__' :

    ### Test
    cats = Cats()
    cat_count = len(cats)
    print("Load {count} cat data.".format(count = len(cats)))

    ### Get cat path
    import cv2
    import random
    idx = random.randint(0, cat_count - 1)
    img_path = cats.get_cat_path(idx)
    rect = cats.get_cat_face(idx)
    print("Cat face ... {}".format(rect))

    ### Display cat
    print("Display '{path}' cat... (Quit : q)".format(path = img_path))
    img = cv2.imread(img_path)
    cv2.imshow("Cat", img)
    while True :
        key = cv2.waitKey(30)
        if key == ord('q') :
            break


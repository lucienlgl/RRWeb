# -*- coding:utf-8 -*-
from __future__ import (absolute_import, division, print_function, unicode_literals)
import os
import io
from surprise import KNNBaseline, Reader
from surprise import Dataset
import logging
from RRWeb.settings import BASE_DIR

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')

# 训练推荐模型 步骤:1
def getSimModle():
    # 载入Restaurants数据集
    # 指定文件路径
    file_path = os.path.expanduser(BASE_DIR + '/rrsite/static/rrsite/reviews.txt')
    # 指定文件格式
    reader = Reader(line_format='item user rating timestamp', sep='\t')
    # 从文件读取数据
    data = Dataset.load_from_file(file_path, reader=reader)

    trainset = data.build_full_trainset()
    #使用pearson_baseline方式计算相似度  False以item为基准计算相似度 本例为餐厅之间的相似度
    sim_options = {'name': 'pearson_baseline', 'user_based': False}
    ##使用KNNBaseline算法
    algo = KNNBaseline(sim_options=sim_options)
    #训练模型
    algo.train(trainset)
    return algo


# 获取id到name的互相映射  步骤:2
def read_item_names():
    """
    获取餐厅名到餐厅id 和 餐厅id到餐厅名的映射
    """
    file_name = (os.path.expanduser('~') +
                 '/.surprise_data/ml-100k/ml-100k/u.item')
    rid_to_name = {}
    name_to_rid = {}
    with io.open(file_name, 'r', encoding='ISO-8859-1') as f:
        for line in f:
            line = line.split('|')
            rid_to_name[line[0]] = line[1]
            name_to_rid[line[1]] = line[0]
    return rid_to_name, name_to_rid


# 基于之前训练的模型 进行相关餐厅的推荐  步骤：3
def showSimilarRestaurants(algo, id):
    # 获得餐厅Toy Story (1995)的raw_id
    raw_id = id
    logging.debug('raw_id=' + raw_id)
    #把餐厅的raw_id转换为模型的内部id
    inner_id = algo.trainset.to_inner_iid(raw_id)
    logging.debug('inner_id=' + str(inner_id))
    #通过模型获取推荐餐厅 这里设置的是10部
    neighbors = algo.get_neighbors(inner_id, 10)
    logging.debug('neighbors_ids=' + str(neighbors))
    #模型内部id转换为实际餐厅id
    neighbors_raw_ids = [algo.trainset.to_raw_iid(inner_id) for inner_id in neighbors]
    #通过餐厅id列表 或得餐厅推荐列表
    #neighbors_restaurants = [rid_to_name[raw_id] for raw_id in neighbors_raw_ids]
    print('The 10 nearest neighbors of Toy Story are:')
    for Restaurant in neighbors_raw_ids:
        print(Restaurant)


if __name__ == '__main__':
    # 获取id到name的互相映射
    #rid_to_name, name_to_rid = read_item_names()

    # 训练推荐模型
    #algo = getSimModle()

    ##显示相关餐厅
    #showSimilarRestaurants(algo, "lKq4Qsz13FDcAVgp49uukQ")

    file = open(BASE_DIR + '/rrsite/static/rrsite/reviews.txt')
    for line in file:
        pass
    file.close()
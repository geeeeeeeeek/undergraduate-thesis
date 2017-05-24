# -*- coding: utf-8 -*-
from __future__ import division

human_selections = {
    '1795219': [['草坪', '市中心', '法式', '跳舞', '放风筝', '回忆', '雁荡', '公馆', '思南路', '玫瑰园'],
    ['法式', '公馆', '玫瑰园', '市中心', '草坪', '家宅', '雕像', '租界', '梧桐树', '园林']],
    '1795246': [['温室', '联票', '樱花', '盆景园', '盆景', '百色', '套票', '花卉', '排队', '桃花'],
    ['迷你', '盆景园', '温室', '交通', '花卉', '联票', '品种', '盆景', '桃花', '樱花']],
    '83506688': [['生态', '工业', '人文景观', '鹦鹉螺', '宠物', '植树', '观花', '文化', '水体', '氧气'],
    ['初具规模', '工业', '生态', '人文', '人文景观', '工业', '健身', '鹦鹉螺', '休闲', '运动']],
    '1906915': [['小孩子', '免费', '小朋友', '儿童乐园', '运动', '适宜', '跑步', '空气', '老年人', '散散步'],
    ['儿童乐园', '小朋友', '免费', '小孩子', '小时候', '老年人', '居民', '散散步', '绿化', '锻炼身体']],
    # '2661205': [['绿地', '花球', '史话', '设计', '森林', '竹影', '鸭子', '建筑', '夜色', '草坪'],
    # ['油菜花', '樱花', '宁静', '草坪', '居民', '锻炼', '空气', '免费', '鸭子', '黑天鹅']]
}

import os

def get_precision(algorithm_selections):
    counter = 0
    for i in xrange(len(algorithm_selections)):
        if algorithm_selections[i] in human_selections[key][0]:
            counter += 1
        if algorithm_selections[i] in human_selections[key][1]:
            counter += 1
    return counter /20

all_algorithms = {'tf_idf_selections': 0, 'tf_idf_pos_selections': 0, 'tf_idf_all_selections': 0, 'textrank_selections': 0}
for key, value in human_selections.iteritems():
    print '###' + key + '###'
    tf_idf_path = 'assets/shanghai_parks_poi_reviews_tf_idf/tf_idf/{k}'.format(k=key)
    tf_idf_selections = []
    with open(tf_idf_path, 'r') as fp:
        for i in xrange(10):
            line = fp.readline().strip()
            tf_idf_selections.append(line.split()[0])
    
    precision = get_precision(tf_idf_selections)
    print 'TF-IDF Precision: ',
    print precision
    all_algorithms['tf_idf_selections'] += precision


    tf_idf_pos_path = 'assets/shanghai_parks_poi_reviews_pseg/tf_idf/{k}'.format(k=key)
    tf_idf_pos_selections = []
    with open(tf_idf_pos_path, 'r') as fp:
        for i in xrange(10):
            line = fp.readline().strip()
            tf_idf_pos_selections.append(line.split()[0])

    precision = get_precision(tf_idf_pos_selections)
    print 'TF-IDF (With Pos) Precision: ',
    print precision
    all_algorithms['tf_idf_pos_selections'] += precision


    tf_idf_all_path = 'assets/shanghai_parks_poi_reviews_extract_keywords/segments/{k}'.format(k=key)
    with open(tf_idf_all_path, 'r') as fp:
        tf_idf_all_selections = fp.readline().split()
    
    precision = get_precision(tf_idf_all_selections)
    print 'TF-IDF (All Documents) Precision: ',
    print precision
    all_algorithms['tf_idf_all_selections'] += precision

    textrank_path = 'assets/shanghai_parks_poi_reviews_text_rank/segments/{k}'.format(k=key)
    with open(textrank_path, 'r') as fp:
        textrank_selections = fp.readline().split()
    
    precision = get_precision(textrank_selections)
    print 'Text Rank Precision: ',
    print precision
    all_algorithms['textrank_selections'] += precision

print '###Mean###'
for key, value in all_algorithms.iteritems():
    print key,
    print ': ',
    print value / 4
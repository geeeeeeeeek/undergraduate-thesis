# -*- coding: utf-8 -*-
from __future__ import division

import logging
import jieba
import os
import collections
import math

logger = logging.getLogger(__name__)

class KeywordExtractor:
    def __init__(self, section):
        self.name = section
        self.tf_dict = {}
        self.idf_meta = collections.Counter()
    
    def do(self):
        self.read_stop_words()

        dir_path = {
            'input': '../poi-crawler/assets/{n}'.format(n=self.name),
            'output': 'assets/{n}'.format(n=self.name),
            'seg_output': 'assets/{n}/segments'.format(n=self.name),
            'tf_output': 'assets/{n}/term_frequency'.format(n=self.name),
            'tf_idf_output': 'assets/{n}/tf_idf'.format(n=self.name)
        }

        if not os.path.exists(dir_path['output']):
            os.mkdir(dir_path['output'])

        for key, value in dir_path.iteritems():
            if not os.path.exists(value):
                os.mkdir(value)

        # Iterate over reviews fetched previously
        document_number = 0
        for filename in os.listdir(dir_path['input']):
            number = filename.split('.')[0]
            # Read review body
            with open(os.path.join(dir_path['input'], filename), 'r') as fp:
                review_body = fp.read()

            # Split document into segments
            seg_list = self.split_words(review_body)
            with open(os.path.join(dir_path['seg_output'], filename), 'w+') as fp:
                fp.write(' '.join(seg_list).encode('utf-8'))

            # Count term frequency
            self.tf_dict[number] = self.count_term_frequency(seg_list)
            with open(os.path.join(dir_path['tf_output'], filename), 'w+') as fp:
                fp.write('\n'.join([key + ' ' + str(value) for key, value in self.tf_dict[number].most_common(100)]).encode('utf-8'))

            # Count inverse document frequency
            self.count_inverse_document_frequency(self.tf_dict[number])
            document_number += 1

        # Generate idf-meta
        with open(os.path.join(dir_path['output'], 'idf_meta.txt'), 'w+') as fp:
            fp.write('\n'.join([key + ' ' + str(value) for key, value in self.idf_meta.most_common(1000)]).encode('utf-8'))
        
        # Calculate tf-idf
        for filename in os.listdir(dir_path['input']):
            number = filename.split('.')[0]
            tf_idf_list = self.calculate_tf_idf(number, document_number)

            with open(os.path.join(dir_path['tf_idf_output'], filename), 'w+') as fp:
                fp.write('\n'.join([key + ' ' + str(value) for key, value in tf_idf_list]).encode('utf-8'))

    def read_stop_words(self):
        self.stop_words = []
        with open('assets/stop_words.txt', 'r') as fp:
            content = fp.readlines()
            self.stop_words += [x.decode('utf-8').strip() for x in content]

    def split_words(self, review_body):
        # Cut the entire review body and remove stop words
        seg_list = jieba.cut(review_body)
        return [
            x for x in seg_list if x.strip() not in self.stop_words 
            and len(x) > 1 
            and x[0] != '一'.decode('utf-8')
            and x[0] != '哈'.decode('utf-8')
            and not x[-1].isdigit()]

    def count_term_frequency(self, seg_list):
        return collections.Counter(seg_list)

    def count_inverse_document_frequency(self, counter):
        self.idf_meta += collections.Counter(counter.keys())

    def calculate_tf_idf(self, number, document_number):
        tf_counter = self.tf_dict[number]
        if len(tf_counter.most_common(1)):
            most_common_word, most_common_total = tf_counter.most_common(1)[0]

        tf_idf_list = []
        for word in tf_counter:
            tf = tf_counter[word] / most_common_total
            idf = math.log(document_number / (self.idf_meta[word] + 1))
            tf_idf = tf * idf
            tf_idf_list.append((word, tf_idf))
        return sorted(tf_idf_list, key=lambda x: x[1], reverse=True)
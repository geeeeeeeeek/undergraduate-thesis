import logging
import jieba
import os
import collections

logger = logging.getLogger(__name__)

class KeywordExtractor:
    def __init__(self, section):
        self.name = section
        self.tf_dict = {}
        self.tf_meta = collections.Counter()
    
    def do(self):
        self.read_stop_words()

        seg_output_dir_path = 'assets/{n}/segments'.format(n=self.name)
        if not os.path.exists(seg_output_dir_path):
            os.mkdir(seg_output_dir_path)

        tf_output_dir_path = 'assets/{n}/term_frequency'.format(n=self.name)
        if not os.path.exists(tf_output_dir_path):
            os.mkdir(tf_output_dir_path)

        # Iterate over reviews fetched previously
        input_dir_path = '../poi-crawler/assets/{n}'.format(n=self.name)
        for filename in os.listdir(input_dir_path):
            number = filename.split('.')[0]
            with open(os.path.join(input_dir_path, filename), 'r') as fp:
                review_body = fp.read()

            seg_list = self.split_words(review_body)
            with open(os.path.join(seg_output_dir_path, filename), 'w+') as fp:
                fp.write(' '.join(seg_list).encode('utf-8'))

            self.tf_dict[number] = self.count_term_frequency(seg_list)
            self.tf_meta += self.tf_dict[number]
            with open(os.path.join(tf_output_dir_path, filename), 'w+') as fp:
                fp.write('\n'.join([key + ' ' + str(value) for key, value in self.tf_dict[number].most_common(100)]).encode('utf-8'))

        # Generate meta-data
        with open(os.path.join(tf_output_dir_path, 'metadata'), 'w+') as fp:
                fp.write('\n'.join([key + ' ' + str(value) for key, value in self.tf_meta.most_common(1000)]).encode('utf-8'))

    def read_stop_words(self):
        self.stop_words = []
        with open('assets/stop_words.txt', 'r') as fp:
            content = fp.readlines()
            self.stop_words += [x.decode('utf-8').strip() for x in content]

    def split_words(self, review_body):
        # Cut the entire review body and remove stop words
        seg_list = jieba.cut(review_body)
        return [x for x in seg_list if x.strip() not in self.stop_words]

    def count_term_frequency(self, seg_list):
        return collections.Counter(seg_list)

    def generate_word_frequency_dict(self):
        pass

    def select_keywords(self):
        pass
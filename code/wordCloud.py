#!/usr/bin/python
# -*- coding:utf8 -*- 
import jieba
import re, csv
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

def segment_comment(srcPath, destPath):

    with open(srcPath,'r',encoding='utf-8') as rdata:
        csv_read = csv.reader(rdata)
        col = [row[0] for row in csv_read]
        # print(col)

    with open(destPath, 'w', encoding='utf-8') as data:
        data.write(str(col))

# TODO 
# 1. 把中文挑出来/去掉符号和网址
# 2. jieba去切分
# 3. 切分后写进txt
# 4. wordCloud
    new_data = re.findall('[\u4e00-\u9fa5]+', data, re.S)
    new_data = ' '.join(new_data)
    print(new_data)


if __name__ == '__main__':
    # segment_comment('F:/1_University/3_大三/1NLP/crawl-and-analyze-short-text-information/data/commentInfo.csv','F:/1_University/3_大三/1NLP/demo.txt')
    segment_comment('F:/1_University/3_大三/1NLP/commentInfo.csv','F:/1_University/3_大三/1NLP/demo.txt')
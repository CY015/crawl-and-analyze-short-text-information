#!/usr/bin/python
# -*- coding:utf8 -*- 

#                     _ooOoo_
#                    o8888888o
#                    88" . "88
#                    (| -_- |)
#                    O\  =  /O
#                 ____/`---'\____
#               .'  \\|     |//  `.
#             /  \\|||  :  |||//  \
#             /  _||||| -:- |||||-  \
#             |   | \\\  -  /// |   |
#             | \_|  ''\---/''  |   |
#             \  .-\__  `-`  ___/-. /
#           ___`. .'  /--.--\  `. . __
#        ."" '<  `.___\_<|>_/___.'  >'"".
#       | | :  `- \`.;`\ _ /`;.`/ - ` : | |
#       \  \ `-.   \_ __\ /__ _/   .-` /  /
#  ======`-.____`-.___\_____/___.-`____.-'======
#                     `=---='
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#                老爷保号   永无Bug
#               Parying for no bugs


import re, os, sys
import csv
import jieba
# TODO 和词典里的去重
#     

def readCorpus(file):
    with open(file, 'r', encoding='utf_16') as f:
        # print(f.read())
        word = re.findall(r'\【.*?\】', f.read(), re.S)
        words = re.findall('[\u4e00-\u9fa5]+', str(word), re.S)

    return words


def removeDuplication(originalDict, cusCorpus):
    # 读取评论数据
    with open(cusCorpus,'r',encoding='utf-8') as rdata:
        csv_read = csv.reader(rdata)
        col = [row[0] for row in csv_read]
        
        # 预处理 只挑出来中文
        new_data = re.findall('[\u4e00-\u9fa5]+', str(col), re.S)

    # 清洗评论数据
    # 分词 精准模式
    word = jieba.cut(str(new_data), cut_all=False)
    # 分词 搜索引擎模式
    # word = jieba.cut_for_search(str(new_data))
    
    # 去掉重复字、词语并截断10个字
    rWord = []
    for w in word:
        if w not in rWord:
            rWord.append(w[:9])
            # if len(w) > 10:
            #     rWord.append(w[:9])
            #     continue
            # rWord.append(w)

    # 把切分的词语写进txt
    # ndata = ' '.join(rWord)
    # with open('../data/originalComment_searchmode.txt','w',encoding='utf-8') as f:
    #     f.write(ndata)

    # 和现代汉语词典中相同的去除
    newWord = []
    for x in rWord:
        if x not in originalDict:
            newWord.append(x)
    print(newWord)


if __name__ == '__main__':
    words = readCorpus('../data/originDict.txt')
    removeDuplication(words, '../data/raw/commentInfo_800760067.csv')
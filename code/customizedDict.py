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

import re, os, sys, time
import csv
import json

import jieba
import pandas as pd
from aip import AipNlp


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

    # 和现代汉语词典中相同的去除
    newWord = []
    for x in rWord:
        if x not in originalDict:
            newWord.append(x)

    # 把新词语写进txt
    # ndata = ' '.join(rWord)
    # with open('../data/originalComment_searchmode.txt','w',encoding='utf-8') as f:
    #     f.write(str(newWord))

    # print(len(newWord))     # 19306
    return newWord


# TODO
# KNN用Annoy实现 TF-IDF评估
# 用例句测试词典分词效果
# https://blog.csdn.net/shuihupo/article/details/85162237
# https://blog.csdn.net/churximi/article/details/51472300?utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromMachineLearnPai2%7Edefault-2.control&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromMachineLearnPai2%7Edefault-2.control

# word2vec(调用百度API) 
def wordToVec(wordList):
    # APPID AK SK  在应用控制台可以看 
    APP_ID = '24413983'
    API_KEY = 'jOuooWybOgN6d0rHa2noGlyU'
    SECRET_KEY = 'UYEz0dW5Z3W66BOKmU6fLxPe8pd6BXLy'

    client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

    wv = []
    noneResult = []
    k = 1
    for word in wordList:
        if k % 2 == 0:
            time.sleep(1)
        try:
            re = json.dumps(client.wordEmbedding(word))
            vec = json.loads(re)
            k = k + 1 
            # 存下词语和向量
            if len(vec['vec']) > 0:
                wv.append([word, vec["vec"]])
        except:
            if "error_code" in vec:
                noneResult.append([word, vec["error_code"]])
                print(word)
            else:
                noneResult.append([word, -1])
                time.sleep(2)
                continue

        # test
        # if k == 10:
        #     break

    # 记录没有vec的词语
    df_error = pd.DataFrame(noneResult, columns=['word', 'error_code'])
    df_error.to_csv('../data/dict/error_word_vec_Dict.csv', index=False, encoding='utf_8_sig')
    # 记录词语和vec
    df = pd.DataFrame(wv, columns=['word', 'vector'])
    df.to_csv('../data/dict/word_vec_Dict.csv', index=False, encoding='utf_8_sig')  


if __name__ == '__main__':
    words = readCorpus('../data/originDict.txt')
    # print(len(words))   # 64847
    # newWord = removeDuplication(words, '../data/raw/commentInfo_800760067.csv')
    wordToVec(words)
    # wordToVec(newWord)
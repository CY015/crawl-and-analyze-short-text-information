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
import logging

import jieba
import jieba.analyse
import pandas as pd
from gensim.models import word2vec, Word2Vec

# 把词典中的词语取出
def readCorpus(file):
    with open(file, 'r', encoding='utf_16') as f:
        word = re.findall(r'\【.*?\】', f.read(), re.S)
        words = re.findall('[\u4e00-\u9fa5]+', str(word), re.S)

    with open('../data/dict/Dict.txt', 'w', encoding='utf_16') as dic:
        dic.writelines('\n'.join(words))
    return words

# 去重
def removeDuplication(originalDict, cusCorpus):
    # 读取评论数据
    with open(cusCorpus,'r',encoding='utf-8') as rdata:
        csv_read = csv.reader(rdata)
        col = [row[0] for row in csv_read]
        
        # 预处理 只挑出来中文
        new_data = re.findall('[\u4e00-\u9fa5]+', str(col), re.S)

    # 清洗评论数据
    # 分词 精准模式
    word = jieba.cut(' '.join(new_data), cut_all=False)
    
    # 去掉重复字、词语
    rWord = []
    for w in word:
        if w not in rWord:
            rWord.append(w)

    # 和现代汉语词典中相同的去除
    newWord = []
    for x in rWord:
        if x not in originalDict:
            newWord.append(x)

    # 把每句话的新词语一行行写进txt
    # ndata = '\n'.join(newWord)
    # with open('../data/Comment_duplicate.txt','w',encoding='utf_8') as f:
    #     f.writelines(ndata)

    return newWord


# TODO
# KNN用Annoy实现 TF-IDF评估
# 用例句测试词典分词效果
# https://blog.csdn.net/shuihupo/article/details/85162237
# https://www.cnblogs.com/pinard/p/7278324.html


# word2vec(垃圾百度词向量API) 
def wordToVec(wordList):
    # # 生成通用词典的vec
    # with open('../data/dict/Dict.txt', 'r', encoding='utf_16') as f:
    #     sentences = word2vec.LineSentence(f)

    #     # 生成模型
    #     model = word2vec.Word2Vec(sentences, hs=1, min_count=1, window=5, size=50)

    #     wv = []
    #     for word in wordList:
    #         vec = model[word]
    #         wv.append([word, vec]) 
    #     df = pd.DataFrame(wv, columns=['word', 'vector'])
    #     df.to_csv('../data/dict/word_vec_Dict.csv', index=False, encoding='utf_16')  
    

    with open('../data/raw/commentInfo_800760067.csv','r',encoding='utf_8') as rdata:
        csv_read = csv.reader(rdata)
        col = [row[0] for row in csv_read]
    
        new_data = re.findall('[\u4e00-\u9fa5]+', str(col), re.S)

        w = jieba.cut('\n'.join(new_data), cut_all=False)

        with open('../data/Comment.txt', 'w', encoding="utf_8") as f:
            f.writelines(' '.join(w))

    # 评论分词后的vec
    with open('../data/Comment.txt', 'r', encoding='utf_8') as f2:
        sentences2 = word2vec.LineSentence(f2)
        model = word2vec.Word2Vec(sentences2, hs=1, min_count=1, window=5, size=50)

        wv_C = []
        for word in wordList:
            if word == '\n' or word == ' ':
                continue
            # if word not in wv_C:
            vec = model[word]
            wv_C.append([word, vec]) 
        df = pd.DataFrame(wv_C, columns=['word', 'vector'])
        df.to_csv('../data/dict/word_vec_Comment.csv', index=False, encoding='utf_8_sig')  


# TF-IDF评估
def TF_IDF_jieba():
    # 设置停用词
    jieba.analyse.set_stop_words('../data/dict/stopwords.txt')
    with open('../data/Comment.txt', 'r', encoding='utf_8') as f:
        topk = jieba.analyse.extract_tags(f.read(), topK=20)

    with open('../data/dict/Dict.txt', 'r', encoding='utf_16') as dic:
        dictionary = dic.read().splitlines()

    newWords = []
    for word in topk:
        if word not in dictionary:
            newWords.append(word)
    
    with open('../data/dict/cusDict.txt', 'a+', encoding='utf_16') as newdict:
        newdict.write('\n')
        for nword in newWords:
            # print(nword)
            newdict.write(nword + '\n')
    # print(', '.join(topk)) # 冰冰，冰冰的，我的心，星星，老婆，粉丝，百万，视频，播放，喜欢

# 测试分词效果
def test():
    print('/'.join(jieba.cut('天冷了，我的心是冰冰的')))
    jieba.load_userdict('../data/dict/cusDict.txt')
    print('/'.join(jieba.cut('天冷了，我的心是冰冰的')))

if __name__ == '__main__':
    # 确保jieba分出来这些名字
    # 在测试时注释掉下面的词
    jieba.add_word("王冰冰")
    jieba.add_word("冰冰")
    jieba.add_word("冰冰姐")
    jieba.add_word("喵酱")
    jieba.add_word("吃花椒")
    jieba.add_word("吃花椒的喵酱")
    jieba.add_word("老婆")
    jieba.add_word("何同学")
    jieba.add_word("饼叔")
    jieba.add_word("食贫道")
    jieba.add_word("毕导")
    jieba.add_word("冰冰的")
    jieba.add_word("我的心")

    words = readCorpus('../data/originDict.txt')    #len(words)   # 64847
    newWord = removeDuplication(words, '../data/raw/commentInfo_800760067.csv')
    # words是词典的
    # newWord是评论
    # 使用时记得在wordToVec中注释
    wordToVec(words)
    wordToVec(newWord)
    TF_IDF_jieba()
    test()
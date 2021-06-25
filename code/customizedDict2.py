import csv, re
import jieba 
import jieba.analyse
from gensim.models import word2vec
from gensim.test.utils import common_texts, get_tmpfile


# with open('../data/raw/commentInfo_800760067.csv','r',encoding='utf-8') as rdata:
#     csv_read = csv.reader(rdata)
#     col = [row[0] for row in csv_read]
    
#     new_data = re.findall('[\u4e00-\u9fa5]+', str(col), re.S)
#     ndata = '\n'.join(new_data)

#     w = jieba.cut(ndata, cut_all=False)
#     words = ' '.join(w)

#     with open('../data/Comment.txt', 'w', encoding="utf_8") as f:
#         f.writelines(words)

def TF_IDF_jieba():
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

    # 设置停用词
    jieba.analyse.set_stop_words('../data/dict/stopwords.txt')
    with open('../data/originalComment.txt', 'r', encoding="utf_8") as f:
        topk = jieba.analyse.extract_tags(f.read(), topK=10)

    print(', '.join(topk))  # 冰冰，冰冰的，我的心，星星，老婆，粉丝，百万，视频，播放，喜欢


def wordToVec():
    with open('../data/Comment.txt', 'r', encoding='utf_8') as f:
        sentences =  word2vec.LineSentence(f)

        # 加载模型    
        model = word2vec.Word2Vec.load('../data/models/word2vec_50dim.model')
        # # 生成模型
        # model = word2vec.Word2Vec(sentences, hs=1, min_count=1, window=5, size=50)
        # model.save('../data/models/word2vec_50dim.model')

    for key in model.wv.similar_by_word('冰冰', topn = 10):
        # if len(key[0]) > 1:
        #     print([key[0],key[1]])
        print([key[0],key[1]])
    print(model['冰冰'])

    # <'冰冰姐', 0.798>    
    # <'我', 0.767>
    # <'她', 0.754>
    # <'老婆', 0.722>
    # <'我们', 0.722>
    # <'你', 0.716>
    # <'王冰冰', 0.696>
    # <'谁', 0.682>
    # <'姐姐', 0.660>
    # <'女朋友', 0.649>


if __name__ == '__main__':
    # TF_IDF_jieba()
    wordToVec()
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
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#               老爷保号   永无Bug

import jieba
import re, csv, collections
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import PIL.Image as image

def save_comment(srcPath, destPath):
    # 增加一些jieba不认识的词语
    jieba.suggest_freq("王冰冰", True)
    jieba.suggest_freq("冰冰", True)
    jieba.suggest_freq("冰冰的", True)
    jieba.suggest_freq("冰冰姐", True)
    jieba.suggest_freq("喵酱", True)
    jieba.suggest_freq("吃花椒", True)
    jieba.suggest_freq("吃花椒的喵酱", True)
    jieba.suggest_freq("老婆", True)
    jieba.suggest_freq("何同学", True)
    jieba.suggest_freq("饼叔", True)
    jieba.suggest_freq("食频道", True)
    jieba.suggest_freq("毕导", True)
    jieba.suggest_freq("我的心", True)

    with open(srcPath,'r',encoding='utf-8') as rdata:
        csv_read = csv.reader(rdata)
        col = [row[0] for row in csv_read]

    with open(destPath, 'w', encoding='utf-8') as data:

        # 预处理 只挑出来中文
        new_data = re.findall('[\u4e00-\u9fa5]+', str(col), re.S)

        # 分词
        words = jieba.cut(' '.join(new_data), cut_all=False)

        ndata = ''.join(words)
        data.write(ndata)


def generate_wordCloud(textPath, wordCloudPath, ice_mask):

    ice_cloud = WordCloud(
        background_color='white',
        width=1366,height=768,
        mask=ice_mask,
        stopwords=STOPWORDS.update(['中奖率','录取','通知书','吧','我','热词','系列','热词系列',' ',
                                    '增加','拉低','怎么','这个','回复','哈哈','的','在','抽个','是',
                                    '啊','这','吗','啦','她','小','你','了','来','抽','知识','知识增加','好家伙','拉低中奖率',
                                    '打','抽我','妙啊','滑稽','呆']),
        font_path='C:\Windows\Fonts\simfang.ttf',
        max_words=250
    )

    words = open(textPath, 'r', encoding='utf-8').read()

    ice_cloud.generate(words)
    ice_cloud.to_file(wordCloudPath)



if __name__ == '__main__':
    # save_comment('../data/raw/commentInfo_800760067.csv', '../data/originalComment.txt')
    Ice_mask = np.array(image.open('../data/content.jpg'))
    generate_wordCloud('../data/Comment.txt', '../data/output/ice.png', Ice_mask)
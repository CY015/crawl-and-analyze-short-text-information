# 爬取B站视频下方评论并进行分析
爬取UP主：[吃花椒的喵酱](https://space.bilibili.com/2026561407/)

## API
### 评论请求url地址
- 浏览器`F12`打开开发者模式，在点开视频向下滚动到评论区时，筛选`JS`可以观察到Request URL, 看下其Resonpse即可看到评论区明细

## 源码(code/)
### 爬取评论(wordCrawl.py)
1. 找到想要爬取的UP主首页，获得她发布的视频列表
2. 通过评论API找到对应视频下的评论
3. 再对应找到子评论

**注意事项**
1. requests有可能会报错`requests.exceptions.ConnectionError: HTTPSConnectionPool(host='api.bilibili.com', port=443)`，原因是由于连接方在一段时间后没有正确答复或连接的主机没有反应，连接尝试失败
2. requests访问后返回的信息`replies`字段是`null`，但在程序里的判断得是`None`而不是`Null`
3. `NoneType object is not subscriptable`在2.中没用过滤全？还会有这个报错
4. 爬取评论中间需要停个1，2秒，不然会触发反爬的机制

### 生成词云(wordCloud.py)
1. 读取csv的`commment`列，把评论读出来，只留中文（会有符号和网址之类的干扰，所以采用只匹配中文）
2. 用`jieba`的精确分词，将分词结果写进txt
3. `WordCloud`生成词云图，自行添加一些*stopwords*（如一些虚词，还有就是系列表情包的名字，如【热词系列】）


### 定制化词典(customizedDict.py)


## 浏览器响应文件demo(response/)
1. `comment_ReplyDemo.json`     第一个视频下的第一页(20条)评论
2. `comment_subReply.json`      是第一个评论下的第一页子评论(10条)
3. `no_Replies.json`            是超出评论页数，无回复
4. `space_videoList.json`       个人空间的视频合集

## 数据(data/)
1. `commentInfo.csv`        评论+评论用户信息的集合
2. `videoList.csv`          发布视频的相关信息
3. `originalComment.txt`    未经过*jieba*切分词的评论
4. `Comment.txt`            经过*jieba*切分后的评论
5. `content.jpg`            词云mask图
### 输出(output/)
* `ice.png`     经过*jieba*切分的词云图
* `iceice.png`  未经过*jieba*切分的词云图
### 词典(dict/)


## Dependency
Python 3.6  
requests  
pandas  
numpy  
jieba  
matplotlib  
wordcloud  
baidu-aip

-----------------------------------------------------------------
**注意**
1. 装包的步骤 `numpy` --> `scipy` --> `gensim` --> `pandas`
   * 装完`pandas`之后会覆盖新的`mkl`的模块(会自动更新`mkl`包版本)，导致`gensim`导入失败，需要重新安装`gensim`
    ```shell
        pip install --force-reinstall gensim-3.8.3-cp36-cp36m-win_amd64.whl
    ```
3. Python3.7的`numpy`轮子有问题，装不上，使用3.6的可以
-----------------------------------------------------------------

## Reference
1. [BiliBili野生API文档](https://github.com/SocialSisterYi/bilibili-API-collect)
2. [Baidu NLP文档](http://ai.baidu.com/ai-doc/NLP/tk6z52b9z)
3. [轮子地址](https://www.lfd.uci.edu/~gohlke/pythonlibs/)
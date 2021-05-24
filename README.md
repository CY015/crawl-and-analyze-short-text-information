# 爬取B站视频下方评论并进行分析
爬取UP主：[吃花椒的喵酱](https://space.bilibili.com/2026561407/)

## API


## 源码(code/)
### 爬取评论(wordCrawl.py)
- 注意事项
1. requests有可能会报错`requests.exceptions.ConnectionError: HTTPSConnectionPool(host='api.bilibili.com', port=443)`，原因是由于连接方在一段时间后没有正确答复或连接的主机没有反应，连接尝试失败
2. requests访问后返回的信息`replies`字段是`null`，但在程序里的判断得是`None`而不是`Null`
3. `NoneType object is not subscriptable`在2.中没用过滤全？还会有这个报错

## 浏览器响应文件demo(response/)
1. `comment_ReplyDemo.json`第一个视频下的第一页(20条)评论
2. `comment_subReply.json`是第一个评论下的第一页子评论(10条)
3. `no_Replies.json`是超出评论页数，无回复
4. `space_videoList.json`个人空间的视频合集

## 数据(data/)
1. `commentInfo.csv`评论+评论用户信息的集合
2. `videoList.csv`发布视频的相关信息
3. `originalComment.txt`评论jieba切分词
4. `content.jpg`词云mask图
### 输出(output/)
- 词云图


## Dependency
Python 3.7  
requests  
pandas
numpy  
jieba  
matplotlib  
wordcloud
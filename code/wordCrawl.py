#!/usr/bin/python
# -*- coding:utf8 -*- 
import os, sys, time
import requests
import json
import pandas as pd

videoData = []
user = []
comment = []

'''
获取指定UP主发布的视频BV号
@param uid: UP主的UID(B站的用户编号)
       size: 该页拉取数目 不填默认为30
       page: 页数
       mode: 搜索模式 默认'pubdate'(最新发布), 'click'(最多播放), 'stow'(最多收藏)
'''
def getAllVideoList(uid, size, page, mode):
    
    # 如果未设定搜索视频模式，则默认搜索度量为时间排序
    if mode == "":
        mode = "pubdate"
    if size == "":
        size = "30"

    # 获取UP主视频列表
    for n in range(1,page+1):
        url = "https://api.bilibili.com/x/space/arc/search?mid=%s&ps=%s&tid=0&pn=%s&keyword=&order=%s&jsonp=jsonp" % (str(uid),size,str(page),mode)
        re = requests.get(url,headers = header).content.decode('utf-8')
        
        # 接收Response文件
        videoInfo = json.loads(re)
        f = open('../space_videoList.json','w',encoding='utf-8')
        f.write(re)
        
        # 读取bv号，av号，视频标题，评论数量，播放数量，弹幕数量
        for i in range(len(videoInfo["data"]["list"]["vlist"])):
            video = videoInfo["data"]["list"]["vlist"][i]
            videoData.append([video["bvid"], video["aid"], video["title"], video["comment"], 
                            video["play"], video["video_review"]])
        
        df = pd.DataFrame(videoData, columns=['BV','AV','Title','Comments_count','Plays_count','Danmu_count'])
        df.to_csv('../data/videoList.csv', index=False, encoding='utf_8_sig')            

'''
获取某视频下的评论
TODO 添加视频av号作为参数，循环爬取?
'''
def getComment():
    # # 循环爬取每个视频的评论
    # for i in range(0,len(avID)):
    #     for j in range(0, page[i]):
    #         # comURL = "https://api.bilibili.com/x/v2/reply?&pn=%s&type=1&oid=%s&sort=1" % (avID[9], str(j))
    #         # comRe = requests.get(comURL,headers = header).text
    #         # print(comRe+'\n\n')

    #         url = 'https://api.bilibili.com/x/v2/reply?type=1&oid=%s&pn=%s&sort=1' % (avID[i],str(j))
    #         r = requests.get(url,headers=header)
    #         # print(r.text)
    #         f = open('./space_response.json','w',encoding='utf-8')
    #         f.write(r.text)

    #         # test
    #         if j == 0:
    #             break
    #     if i == 0:
    #         break

    comURL = 'https://api.bilibili.com/x/v2/reply?&pn=1&type=1&oid=800760067&ps=20&sort=1'
    comRe = requests.get(comURL,headers = header).text
    commentInfo = json.loads(comRe)
    root_count = commentInfo["data"]["page"]["count"]

    # 获取评论页数，这里把页数减少一些, 筛掉一些没用或者有攻击性的? B站会将没用的评论放在最后
    page_count = int(root_count) // 20 - 10

    # 只爬冰冰入驻视频
    for j in range(1, page_count):
        comURL = 'https://api.bilibili.com/x/v2/reply?&pn=%s&type=1&oid=800760067&ps=20&sort=1' % (str(j))
        # time.sleep(1)
        try:
            comRe = requests.get(comURL,headers = header).text
        except:
            continue
        
        commentInfo = json.loads(comRe)
        # 没有评论
        # 写None而不是写Null!
        try:
            if commentInfo["data"]["replies"] == None:
                continue
        except:
            continue

        for m in range(len(commentInfo["data"]["replies"])):
            # 用户id 用户名 用户等级 用户类型(是否为官方认证)
            # -1 普通用户  0 黄色V(B站UP的认证)  1 蓝色V(正规机构的认证)
            userInfo = commentInfo["data"]["replies"][m]["member"]
            user_id = userInfo["mid"]
            user_name = userInfo["uname"]
            user_level = userInfo["level_info"]["current_level"]
            user_verify = userInfo["official_verify"]["type"]

            user.append([user_id, user_name, user_level, user_verify])
            comment.append(commentInfo["data"]["replies"][m]["content"]["message"])
                                    
            # 子评论
            # rpid 根评论用户编号   rcount 子评论总数   subReply_count 子评论页数(舍弃最后一页评论)
            user_rpid = commentInfo["data"]["replies"][m]["rpid"]
            subReply_count = int(commentInfo["data"]["replies"][m]["rcount"]) // 10
            subUser, subComment = getSubComment(800760067, user_rpid, subReply_count)
            comment.extend(subComment)
            user.extend(subUser)
            # 测试爬取第一条评论的子评论
            # if m == 0:
            #     # print(comment)
            #     # print(user)
            #     break 
            
        # 测试
        # if j == 1:
        #     save2File(comment, user)
        #     break
    save2File(comment, user)

'''
获取某评论下的子评论
@param oid: 视频av号  
       rpid: 根评论用户编号  
       pages: 页数  
'''
def getSubComment(oid, rpid, pages):
    # 子评论响应地址demo
    # https://api.bilibili.com/x/v2/reply/reply?&pn=1&type=1&oid=800760067&ps=20&root=3889395859
    subComment = []
    subUser = []
    # 假代理
    # https://blog.csdn.net/c406495762/article/details/60137956
    for k in range(1, pages+1):
        # 防止频繁访问API被封
        time.sleep(1)
        url = 'https://api.bilibili.com/x/v2/reply/reply?&pn=%s&type=1&oid=%s&ps=10&root=%s' % (str(k),str(oid),str(rpid))
        try:
            comRe = requests.get(url, headers = header)
            print(comRe.status_code)
        except:
            continue
            print('服务器主机无响应')
        if comRe.status_code == 412:
            print("请求频繁\n")
            break
        subCommentInfo = json.loads(comRe.text)

        try:
            if subCommentInfo["data"]["replies"] == None:
                break
        except:
            continue
        
        for n in range(len(subCommentInfo["data"]["replies"])):
            subInfo = subCommentInfo["data"]["replies"][n]
            subUser.append([subInfo["member"]["mid"],
                            subInfo["member"]["uname"],
                            subInfo["member"]["level_info"]["current_level"],
                            subInfo["member"]["official_verify"]["type"]
                            ])
            subComment.append(subInfo["content"]["message"])

    return subUser, subComment

# 获取某视频的弹幕
# 
def getDanmu():
    pass

# 存储信息
def save2File(commentList, userList):
    Info = []
    for i in range(len(commentList)):
        sub = []
        sub.append(commentList[i])
        sub.extend(userList[i])

        Info.append(sub)
    title = ['comment','user_id', 'user_name', 'user_level', 'user_verify']
    df = pd.DataFrame(columns=title, data=Info)
    df.to_csv('../data/commentInfo.csv', index=False, encoding='utf_8_sig')

if __name__ == "__main__":
    header = {
        'accept': '*/*',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
    }
    getAllVideoList(2026561407,"",1,"")
    getComment()

    # url = 'https://api.bilibili.com/x/v2/dm/history?type=1&oid='+cid+'&date='+time
    # getDanmu()

#!/usr/bin/python
# -*- coding:utf8 -*- 
import os, sys, time
import requests
import json
import pandas as pd

# 冰冰的关注列表和其关注的关注列表
following = []
followingsf = []

# 获取用户编号为uid的关注列表
def getFollowing(uid, pages):
    if uid == 2026561407 or int(pages) <= 50:
        pages = 1
    else:
        pages = 2

    # 冰冰关注的人的基本信息
    for i in range(1, pages+1):
        print(i)
        followingURL = 'https://api.bilibili.com/x/relation/followings?vmid=%s&pn=%s&ps=50&order=asc&jsonp=jsonp' % (str(uid),str(i))
        Re = requests.get(followingURL, headers = header).text
        Info = json.loads(Re)

        for m in range(len(Info["data"]["list"])):
            user = Info["data"]["list"][m]
            uid = user["mid"]
            uname = user["uname"]
            uverify = user["official_verify"]["type"]

            following.append([uid, uname, uverify])
        # print(''.join(following))
    print('冰冰的关注：\n' + '\n'.join('%s' %id for id in following) + '\n')

    # 冰冰关注的人的关注
    for user in following:
        # print(''.join('%s' %id for id in user))
        fid = user[0]
        print('用户编号:' + str(fid))
        # name = user[1]

        time.sleep(5)
        uCountURL = 'https://api.bilibili.com/x/relation/stat?vmid=%s&jsonp=jsonp' % str(fid)
        uRe = requests.get(uCountURL, headers = header).text
        uInfo = json.loads(uRe)
        fingCount = uInfo["data"]["following"]

        if int(fingCount) <= 50:
            upages = 1
        else:
            upages = 2
        
        for i in range(1, upages+1):
            ufollowingURL = 'https://api.bilibili.com/x/relation/followings?vmid=%s&pn=%s&ps=50&order=asc&jsonp=jsonp' % (str(fid),str(i))
            uRe = requests.get(ufollowingURL, headers = header).text
            uInfo = json.loads(uRe)

            for m in range(len(uInfo["data"]["list"])):
                user = uInfo["data"]["list"][m]
                u_id = user["mid"]
                u_name = user["uname"]
                u_verify = user["official_verify"]["type"]


                followingsf.append([u_id, u_name, u_verify, fid])
    print('\n'.join('%s' %id for id in followingsf))

# 存储用户id 和 认证标签
def saveLabels(flist, fsflist):
    labels = []
    for finfo in flist:
        labels.append([finfo[0], finfo[2]])

    for fsfinfo in fsflist:
        if [fsfinfo[0], fsfinfo[2]] not in labels:
            labels.append([fsfinfo[0], fsfinfo[2]])

    with open('../data/DeepWalk/labels.txt', 'w', encoding='utf_8') as f:
        f.writelines(str(uinfo) + '\n' for uinfo in labels)

# 存储关注关系边
def saveFollowing(flist, fsflist):
    edges = []
    for finfo in flist:
        edges.append([2026561407, finfo[0]])
    for fsfinfo in fsflist:
        edges.append([fsfinfo[-1], fsfinfo[0]])

    with open('../data/DeepWalk/edges.txt', 'w', encoding='utf_8') as f:
        f.writelines(str(edge) + '\n' for edge in edges)


if __name__ == '__main__':
    header = {
        'accept': '*/*',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
    }
    
    # 可以看到关注人数和粉丝数
    CountURL = 'https://api.bilibili.com/x/relation/stat?vmid=2026561407&jsonp=jsonp'
    Re = requests.get(CountURL, headers = header).text
    Info = json.loads(Re)

    fingCount = Info["data"]["following"]

    getFollowing(2026561407, fingCount)
    saveLabels(following, followingsf)
    saveFollowing(following, followingsf)
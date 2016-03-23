#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import logging
import os
import re
import json
# from PIL import Image
# from io import BytesIO
# import itertools
import urllib.parse
import requests

logging.basicConfig(format='%(levelname)s(%(lineno)s): %(message)s')


# 字符串加密解密
def changecode_url(text, trans_dict):
    trans_dict = {re.escape(key): value for key, value in trans_dict.items()}
    pattern = re.compile('|'.join(trans_dict.keys()))
    text = pattern.sub(lambda m: trans_dict[re.escape(m.group(0))], text)
    return text


# 下载图片
def down_pic(url):
    global getNum, failNum
    print(url, end=" load... ")
    name = url.split("/")[-1]
    # print(name)
    if len(name) > 10:
        name = name[-10:]
    # print(name)
    # print(url)
    try:
        r = requests.get(url, stream=True, timeout=4)
        # if r.status_code!=200:
        #     return
        pic_path = os.path.join(path, name)
        with open(pic_path, 'wb') as f:
            for chunk in r.iter_content(1024 * 10):
                f.write(chunk)
        # im = Image.open(BytesIO(requests.get(url).content))
        # im.save(os.path.join(path,name))
        print('下载成功')
        getNum += 1
    except:
        print('=== 下载失败 ===')
        failNum += 1
        return


def down_page(n=10):
    temp_url = 'http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%E9%AB%98%E6%B8%85%E5%8A%A8%E6%BC%AB%E5%9B%BE%E7%89%87&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&word=%E9%AB%98%E6%B8%85%E5%8A%A8%E6%BC%AB%E5%9B%BE%E7%89%87&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&pn={pn}&rn=30&gsm=200003c'
    for page in (temp_url.format(pn=x * 30) for x in range(20, n)):
        r = requests.get(page)
        r.encoding = 'utf-8'
        for url in r.json()['data'][:30]:
            try:
                url = url['objURL']
            except KeyError:
                continue
            # print(url)
            for dic in decode_dict:
                url = changecode_url(url, dic)
            down_pic(url)



decode_dict = json.load(open('decode.data'))
getNum=0
failNum=0
path = r'd:\BaiduPic'
if not os.path.isdir(path):
    os.makedirs(path)
down_page(70)
print('供下载成功{}张，下载失败{}张'.format(getNum,failNum))

# checkurl='http://img3.3lian.com/2013/s1/90/d/117.jpg'
# r=requests.get(checkurl,stream=True)
# # im=Image.open(BytesIO(r.content))
# # im.show()
# # im.save('test.jpg')
# with open('test.jpg','wb') as f:
#     for chunk in r.iter_content(1024*10):
#         f.write(chunk)
# print(r.status_code)
# down_pic(checkurl)

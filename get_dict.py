#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import logging
import requests
import re
import string
import time
import json

logging.basicConfig(format='%(levelname)s(%(lineno)s): %(message)s')

trans_dict = {}

checkList = string.ascii_letters + string.digits + ':/.'


# 制作真实url与混淆后的url列表，为后续提取字典做准备
def make_url_list():
    source_url = []
    url = 'http://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fr=&sf=1&fmq=1449826069912_R&pv=&ic=0&nc=1&z=&se=&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word=高清动漫图片'
    r = requests.get(url)
    r.encoding = 'utf-8'
    for index, line in enumerate(re.findall(r'"objURL":"(.*?)"', r.text)):
        # print('index:{} line:{}'.format(index,line))
        source_url.append(line)

    after_url = []
    url = 'http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%E9%AB%98%E6%B8%85%E5%8A%A8%E6%BC%AB%E5%9B%BE%E7%89%87&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&word=%E9%AB%98%E6%B8%85%E5%8A%A8%E6%BC%AB%E5%9B%BE%E7%89%87&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&pn=0&rn=30&gsm=200003c'
    r = requests.get(url)
    r.encoding = 'utf-8'
    for index, line in enumerate(r.json()['data']):
        try:
            # print('index:{} line:{}'.format(index,line['objURL']))
            after_url.append(str(line['objURL']))
        except KeyError:
            break
            # after_url.append(str(line['objURL']))
    url_list = []
    for source, after in zip(source_url, after_url):
        url_list.append([source, after])
    return url_list


url_list = make_url_list()

# 观察混淆后的列表，可以很容易获得以下对应关系,制作符号字典
code_dict={}
code_dict['_z&e3B']='.'
code_dict['AzdH3F']='/'
code_dict['_z2C$q']=':'

# 去除这些映射后，剩下的字符与原字符一一对应
# 为后续需要，制作交换dict对象key,value的函数

def swap_dict(d):
    return {value:key for value in d.values() for key in d.keys() if d[key]==value}

encode_dict=swap_dict(trans_dict)
# print(trans_dict)
# print(encode_dict)


# 字符串加密解密
def changecode_url(text, trans_dict):
    trans_dict = {re.escape(key):value for key,value in trans_dict.items()}
    pattern = re.compile('|'.join(trans_dict.keys()))
    text = pattern.sub(lambda m: trans_dict[re.escape(m.group(0))], text)
    return text


# 将特殊符号转换后，剩下字符串与原字符串存在一一对应关系
def extract_dict(url_list=url_list,trans_dict = trans_dict):
    # url_list每个元素的第一个为原链接，第二个为混淆链接，通过提取字典来还原第二链接直到与原链接相同
    for url in url_list:
        url[1]=changecode_url(url[1], code_dict)  # 去掉特殊符号
        for key,value in zip(url[1], url[0]):
            trans_dict[key] = value

# extract_dict()
# print(code_dict)
# print(trans_dict)

# decode_dict = [code_dict,trans_dict]
# json.dump(decode_dict,open('decode.data','w'))

check_str='ippr_z2C$qAzdH3FAzdH3Fbmktzit_z&e3B4wg4wghwg_z&e3Bv54AzdH3FktzitrtvAzdH3Fda8n8dAzdH3FdnnbAzdH3F8_8dbaxbaa_z&e3B3r2'


def decode_str(check_str=check_str):
    decode_data = json.load(open('decode.data'))
    for dic in decode_data:
        check_str=changecode_url(check_str,dic)
        print(check_str)


decode_str()

#制作混淆的字典
# print(decode_data[1])
# encode_dict=[swap_dict(decode_data[1]),swap_dict(decode_data[0])]
# checkstr='http://imga1.pic21.com/bizhi/140226/07916/s04.jpg'
# for i in encode_dict:
#     checkstr=changecode_url(checkstr,i)
# print(checkstr)
# json.dump(encode_dict,open('encode.data','w'))

#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import logging
import re
import itertools
import urllib.parse
import requests

logging.basicConfig(format='%(levelname)s(%(lineno)s): %(message)s')

word = "大航海"
word = urllib.parse.quote(word)
print(word)
url = r'http://image.baidu.com/search/avatarjson?tn=resultjson_com&ie=utf-8&word={word}&cg=wallpaper&pn={pn}&rn=30&itg=0&z=0&lm=-1&ic=0&s=0&st=-1'
urls = (url.format(word=word, pn=x) for x in itertools.count(start=0, step=30))

web = r'http://image.baidu.com/search/avatarjson?tn=resultjsonavatarnew&ie=utf-8&word=%E5%A4%A7%E8%88%AA%E6%B5%B7&cg=wallpaper&pn=0&rn=30&itg=0&z=0&lm=-1&ic=0&s=0&st=-1'

# count = 0
# for link in urls:
#     print(link)
#     count += 1
#     if count>10:
#         break

r = requests.get(web)
r.encoding = 'utf-8'
# print(r.text)
re_url = re.compile(r'"objURL":"(.*?)"')
for pic_url in re_url.findall(r.text):
    print(pic_url)

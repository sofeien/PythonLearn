#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import logging
import os
import re
import json
import urllib.parse
import requests

logging.basicConfig(format='%(levelname)s(%(lineno)s): %(message)s')


class BaiduSpider:
    def __init__(self):
        self.getNum = 0
        self.failNum = 0
        self.decode_dict = json.load(open('decode.data'))
        headers={}
        headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
        # headers['Host'] = 'image.baidu.com'
        headers['Accept'] = 'text/plain, */*; q=0.01'
        headers['Accept-Encoding'] = 'gzip, deflate, sdch'
        headers['Accept-Language'] = 'zh-CN,zh;q=0.8'
        headers['Connection'] = 'keep-alive'
        self.s = requests.Session()
        self.s.headers.update(headers)

    def _changecode(self, text, dic):
        trans_dict = {re.escape(key): value for key, value in dic.items()}
        pattern = re.compile('|'.join(trans_dict.keys()))
        return pattern.sub(lambda m: trans_dict[re.escape(m.group(0))], text)

    def _getpage(self, url_temp, n, path):
        for page in (url_temp.format(pn=x * 30) for x in range(0, n)):
            r = self.s.get(page)
            for url in r.json()['data']:
                try:
                    url = url['objURL']
                except KeyError:
                    break
                for dic in self.decode_dict:
                    url = self._changecode(url, dic)
                self._downpic(url, path)

    def _downpic(self, url, path):
        print(url, end=" loading... ")
        name = url.split('.')[-1]
        # if len(name) > 10:
        #     name = name[-10:]
        name = str(self.getNum + 1) + '.' + name
        try:
            r = self.s.get(url, stream=True, timeout=3)
            # logging.warning(r.status_code)
            if r.status_code != 200:
                raise Exception('not connect')
            pic_path = os.path.join(path, name)
            with open(pic_path, 'wb') as f:
                for chunk in r.iter_content(1024 * 10):
                    f.write(chunk)
                print('下载成功')
                self.getNum += 1
        except:
            print('=== 下载失败 ===')
            self.failNum += 1
            return

    def load(self, url_temp, n=10, path=r'd:\BaiduPic'):
        if not os.path.isdir(path):
            os.makedirs(path)
        self._getpage(url_temp, n, path)
        print('下载成功{}张，下载失败{}张'.format(self.getNum, self.failNum))

url_temp = 'http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%E5%A4%A7%E8%88%AA%E6%B5%B7%E6%97%B6%E4%BB%A3&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&word=%E5%A4%A7%E8%88%AA%E6%B5%B7%E6%97%B6%E4%BB%A3&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&pn={pn}&rn=30&gsm=1e&1458726211852='
BaiduSpider().load(url_temp, n=3)

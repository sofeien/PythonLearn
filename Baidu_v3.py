#coding='utf-8'
from tkinter import *
import requests
import urllib.parse
import os

class BaiduSpider:
    def __init__(self):
        self.getNum = 0
        self.failNum = 0
        self.decode_dict = [{"_z2C$q": ":", "AzdH3F": "/", "_z&e3B": "."}, {"O": "O", "4": "m", "N": "N", "R": "R", "z": "z", "7": "u", "e": "v", "o": "w", "1": "d", "x": "x", "M": "M", "p": "t", "j": "e", "3": "j", "9": "4", "H": "H", "A": "A", "S": "S", "i": "h", "k": "b", "g": "n", "_": "_", "C": "C", "d": "2", "m": "6", "8": "1", ":": ":", "2": "g", "n": "3", "u": "f", "D": "D", "B": "B", "/": "/", "w": "a", "f": "s", ".": ".", "T": "T", "%": "%", "s": "l", "0": "7", "r": "p", "E": "E", "l": "9", "6": "r", "a": "0", "t": "i", "-": "-", "v": "c", "b": "8", "L": "L", "5": "o", "Q": "Q", "c": "5", "=": "=", "h": "k"}]
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
            'Accept': 'text/plain, */*; q=0.01', 'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8', 'Connection': 'keep-alive'}
        self.s = requests.Session()
        self.s.headers.update(headers)
        self.url_temp = 'http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord={word}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&word={word}&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&pn={pn}&rn=30'
        self.url_temp2 = 'http://image.baidu.com/search/avatarjson?tn=resultjsonavatarnew&ie=utf-8&word={word}&cg={cg}&pn={pn}&rn=30&itg=1&z=&fr=&width=&height=&lm=-1&ic=0&s=0&st=-1&gsm=100003c'

    def _changecode(self, text, dic):
        trans_dict = {re.escape(key): value for key, value in dic.items()}
        pattern = re.compile('|'.join(trans_dict.keys()))
        return pattern.sub(lambda m: trans_dict[re.escape(m.group(0))], text)

    def _getpage(self, word, n, size, path, mode, cg):
        if mode == 1:
            generator = (self.url_temp.format(word=urllib.parse.quote(word), size=size, pn=x * 30) for x in range(0, n))
            for page in generator:
                try:
                    r = self.s.get(page)
                except TimeoutError:
                    print('连接超时')
                    return
                r.encoding = 'utf-8'
                for url in r.json()['data']:
                    try:
                        url = url['objURL']
                    except KeyError:
                        break
                    for dic in self.decode_dict:
                        url = self._changecode(url, dic)
                    self._downpic(url, path, word)
        else:
            generator = (self.url_temp2.format(word=urllib.parse.quote(word), cg=cg, pn=x * 30) for x in range(0, n))
            for page in generator:
                try:
                    r = self.s.get(page)
                except TimeoutError:
                    print('连接超时')
                r.encoding = 'utf-8'
                for url in r.json()['imgs']:
                    try:
                        url = url['objURL']
                    except KeyError:
                        break
                    self._downpic(url, path, word)

    def _downpic(self, url, path, word):
        path = os.path.join(path, word)
        if not os.path.isdir(path):
            os.makedirs(path)
        print(url, end=" loading... ")
        name = url.split('.')[-1]
        name = str(self.getNum + 1) + '.' + name
        try:
            r = self.s.get(url, stream=True, timeout=3)
            # logging.warning(r.status_code)
            if r.status_code != 200:
                raise Exception('not connect')
            pic_path = os.path.join(path, name)
            while os.path.isfile(pic_path):
                name = 'new_' + name
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

    # size=[3-‘大尺寸’] [0,''-‘不筛选或自定义尺寸'] [9-‘特大尺寸’] [2-‘中尺寸’]
    # mode [1-普通下载，0-特殊下载]
    # cg ['wallpaper'-'壁纸','head'-'头像']
    def load(self, word, n=1, size=3, path=r'd:\BaiduPic', mode=1, cg='wallpaper'):
        if not os.path.isdir(path):
            os.makedirs(path)
        self._getpage(word, n, size, path, mode, cg)
        return '下载成功{}张，下载失败{}张'.format(self.getNum, self.failNum)

def main():
    global key_word
    global page
    global choice
    global status
    word = key_word.get()
    n = int(page.get())
    status['text']='load...'
    if choice==1:
        result = BaiduSpider().load(word, n=n)
    else:
        result = BaiduSpider().load(word, n=n, mode=0, cg='wallpaper')
    status['text']=result
    # else:
    #     BaiduSpider().load(word, n=n, mode=0, cg='head')


root = Tk()
root.title('百度图片爬虫')
f = Frame(root)
f.pack(padx=10, pady=(10, 5))
f2 = Frame(root)

Label(f, text="关键字:").grid(row=0, padx=5, pady=(0, 5), sticky=E)
key_word = Entry(f)
key_word.grid(row=0, column=1, padx=(0, 5), pady=(0, 5))
Label(f, text="下载页数:").grid(row=1, padx=5)
page = Entry(f)
page.insert(0,'1')
page.grid(row=1, column=1, padx=(0, 5))
f3 = Frame(root)
f3.pack(padx=10)
f2.pack(padx=10, pady=(5, 10))
choice = IntVar()
Radiobutton(f3, text="普通", variable=choice, value=1).grid(row=0, column=0, padx=5)
Radiobutton(f3, text="壁纸", variable=choice, value=2).grid(row=0, column=1, padx=5)
# Radiobutton(f3, text="头像", variable=choice, value=3).grid(row=0, column=2, padx=5)
choice.set(1)
searchBtn = Button(f2, text='搜索', width=20, command=main)
searchBtn.grid(row=0, columnspan=2)
key_word.focus_set()
status = Label(root, text="status")
status.pack(side=BOTTOM, fill=X)
root.mainloop()

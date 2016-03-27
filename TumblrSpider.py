import requests
import re
import os

class TumblrSpider:
    def __init__(self, path=r"d:\PicRoom"):
        self.sourceUrl = ["http://ennui-time.tumblr.com/page/{n}", "http://takedarena-ch.tumblr.com/page/{n}", "http://miaomiaoali.tumblr.com/page/{n}", "http://delicate-asian.tumblr.com/page/{n}","http://jumpinggirlsession.tumblr.com/page/{n}"]
        self.faiList = []
        self.url_re = re.compile(r'src=\"(.*?(?:png|jpg|false|gif))\"')
        self.Path = path
        if not os.path.isdir(path):
            os.makedirs(path)
        return

    def _download(self, picUrl, picPath):
        print(picUrl, end="  ")
        try:
            r = requests.get(picUrl, stream=True, timeout=3)
            with open(picPath,"wb") as f:
                for chunk in r.iter_content(1024*4):
                    f.write(chunk)
            print('下载成功')
            return
        except:
            print('下载失败')
            self.faiList.append((picUrl,picPath))
            return

    def _filterUrl(self, url):
        try:
            r = requests.get(url)
            return list(self.url_re.findall(r.text))
        except:
            print('打开网址 {} 失败'.format(url))
            return

    def _checkPic(self, url, dirPath):
        picName = url.split('/')[-1]
        if picName.startswith("avatar"):
            return 0
        picPath = os.path.join(dirPath, picName)
        if os.path.isfile(picPath):
            return 0
        return picPath

    def download(self, url, needpage=1):
        dirName = url.split(".")[0][len('http://'):]
        dirPath = os.path.join(self.Path, dirName)
        if not os.path.isdir(dirPath):
            os.makedirs(dirPath)
        urllist = [url.format(n=x) for x in range(1, needpage+1)]
        for url in urllist:
            print(url)
            for pic_url in self._filterUrl(url):
                if pic_url.endswith('false'):
                    for new_picurl in self._filterUrl(pic_url):
                        picPath = self._checkPic(new_picurl, dirPath)
                        if not picPath:
                            continue
                        self._download(new_picurl, picPath)
                else:
                    picPath = self._checkPic(pic_url, dirPath)
                    if not picPath:
                        continue
                    self._download(pic_url, picPath)
        self.retryCheck()

    def downlist(self, page=1):
        for url in self.sourceUrl:
            self.download(url, page)
        # self.retryCheck()

    def showSource(self):
        for url in self.sourceUrl:
            print(url[:-8])
    def showFailList(self):
        print(TumblrSpider.failList)
    def retryCheck(self):
        count = len(self.faiList)
        if count>0:
            print('失败链接再次重试:')
            for _ in range(count):
                item = self.faiList.pop()
                self._download(*item)


TumblrSpider().downlist()


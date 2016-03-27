import requests
import re
import os
linkList = ["http://ennui-time.tumblr.com/page/{n}", "http://takedarena-ch.tumblr.com/page/{n}", "http://miaomiaoali.tumblr.com/page/{n}", "http://delicate-asian.tumblr.com/page/{n}","http://jumpinggirlsession.tumblr.com/page/{n}"]
url = linkList[0]
basePath = r"e:\sex"
dirName = url.split(".")[0][len('http://'):]
# print(dirName)
dirPath = os.path.join(basePath,dirName)
if not os.path.isdir(dirPath):
    os.makedirs(dirPath)
n = 4 # 5页
for page in range(1, n+1):
    currentUrl = url.format(n=page)
    print(currentUrl)
    try:
        r = requests.get(currentUrl)
    except:
        print('页面打开失败')
        continue
    # print(r.text)
    pic_re = re.compile(r'src=\"(.*?(?:png|jpg|false|gif))\"')
    for picUrl in pic_re.findall(r.text):
        if picUrl.endswith("false"):
            inside_r=requests.get(picUrl)
            for inside_picUrl in pic_re.findall(inside_r.text):
                picName = inside_picUrl.split('/')[-1]
                if picName.startswith("avatar"):
                    continue
                picPath = os.path.join(dirPath,picName)
                if os.path.isfile(picPath):
                    continue
                print(inside_picUrl, end="   ")
                # print(picName)
                try:
                    r = requests.get(inside_picUrl, stream=True, timeout=5)
                    with open(picPath, 'wb') as f:
                        for chunk in r.iter_content(1024 * 4):
                                f.write(chunk)
                    print('下载成功')
                except:
                    print('下载失败')
                    continue
        else:
            picName = picUrl.split('/')[-1]
            if picName.startswith("avatar"):
                continue
            picPath = os.path.join(dirPath,picName)
            if os.path.isfile(picPath):
                continue
            print(picUrl, end="   ")
            # print(picName)
            try:
                r = requests.get(picUrl, stream=True, timeout=5)
                with open(picPath, 'wb') as f:
                    for chunk in r.iter_content(1024 * 4):
                            f.write(chunk)
                print('下载成功')
            except:
                print('下载失败')
                continue
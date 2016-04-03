import re
from tkinter import *
from tkinter.filedialog import *
from tkinter.ttk import *
import requests
import os
import threading
import json

import time

url_list = []
pic_list = []
fail_list = []
total = 0
current = 0

def find_dir(*args):
    """设置保存文件夹"""
    path.set(askdirectory())
    return

def getframe(u, *args):
    """提取框架地址"""
    global url_list
    try:
        r = requests.get(u)
    except:
        print("网址打开失败")
        return
    frame_re = re.compile(r'src="(.*?false)"')
    for frame in frame_re.findall(r.text):
        # print("提取框架地址:{}".format(frame))
        url_list.append(frame)

def savepic(u, *args):
    """保存图片"""
    global fail_list
    print("打开图片地址:{}".format(u), end="  ")
    picname = u.split("/")[-1]
    picpath = os.path.join(os.path.normpath(path.get()), picname)
    try:
        r = requests.get(u, stream=True, timeout=5)
        with open(picpath, "wb") as f:
            for chunk in r.iter_content(1024*4):
                f.write(chunk)
        print("下载成功")
    except:
        fail_list.append(u)
        print('下载失败')

def getpic(u):
    """提取图片地址"""
    global pic_list
    pic_re = re.compile(r'src="(.*?(?:png|jpg|gif|jpeg))"')
    try:
        r = requests.get(u)
        for pic in pic_re.findall(r.text):
            # print("提取图片地址:{}".format(pic))
            pic_list.append(pic)
    except:
        print("提取图片地址失败:{}".format(u))
        return

def loadStatus(*args):
    global total,current
    while current<=total:
        # print("打印进度{}/{}".format(current,total))
        if current==total or total==0:
            p["value"] = 100
            root.update()
            break
        p["value"] = current*100/total
        root.update()
        time.sleep(0.5)

def showStatus():
    threading.Thread(target=loadStatus).start()
    return

def downpic(*args):
    """下载网页图片"""
    global url_list, pic_list, fail_list, total, current
    print("打开网址:{}".format(url.get()))
    getpic(url.get())
    getframe(url.get())
    for frame in url_list:
        getpic(frame)
    total = len(pic_list)
    print("照片总数{}".format(total))
    # threading.Thread(target=loadStatus).start()
    showStatus()
    for index,pic in enumerate(pic_list):
        savepic(pic)
        current = index+1
    retry = len(fail_list)
    if retry>0:
        print('失败链接再次下载')
    for i in range(retry):
        u = fail_list.pop()
        savepic(u)
    print(fail_list)
    if len(fail_list)>0:
        json.dump(fail_list,open(os.path.join(os.path.normpath(path.get()),'log.txt'),"w"))
    url_list = []
    pic_list = []
    fail_list = []
    total = 0
    current = 0
    print("下载结束")

def main(*args):
    p["value"] = 0
    root.update()
    print("下载开始")
    threading.Thread(target=downpic).start()
    # threading.Thread(target=loadStatus).start()
    return

root = Tk()
root.title('网页图片爬虫')
root.geometry("400x120+100+100")
Label(root, text="URL:").grid(row=1,column=1)
url = StringVar()
entry = Entry(root, textvariable=url)
entry.grid(row=1, column=2, sticky="WE")
# Label(root,text="保存路径:").grid(row=2, column=1)
path = StringVar()
Entry(root, textvariable=path, state=["readonly"]).grid(row=2, column=2, sticky="WE")
path.set(r'C:\Users\cadencheng\Desktop\新建文件夹')
Button(root, text="选择文件夹", command=find_dir).grid(row=2, column=1)
for child in root.winfo_children():
    child.grid(padx=5, pady=5)
Button(root, text="下      载", command=main).grid(row=3, column=1, columnspan=2)
# 添加进度条
p = Progressbar(root,mode="determinate", orient=HORIZONTAL)
p.grid(row=4,column=1,columnspan=2,sticky="WE",pady=(5,0))
p["maximum"] = 100
p["value"] = 0
entry.focus()
root.columnconfigure(2,weight=1)
root.bind("<Return>",main)
root.mainloop()
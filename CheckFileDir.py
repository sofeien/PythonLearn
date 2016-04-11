#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"选择盘符或选择文件夹，在桌面生成Log文件，将选择目录下文件按由大到小排列"

import os
from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import *
import threading

filelist = []

def formatSize(size, is1024=True):
    "格式化文件大小"
    formatUnit = {1024: ['KB', 'MB', 'GB', 'TB'], 1000: ['KiB', 'MiB', 'GiB', 'TiB']}
    block = 1024 if is1024 else 1000
    for unit in formatUnit[block]:
        size /= block
        if size < block:
            return "{0:.2f}{1}".format(size, unit)
    raise ValueError('输入数字过大')

def scanDir(beginPath='E:\\'):
    # print('Current Path: {}'.format(beginPath))
    try:
        for item in os.scandir(beginPath):
            if item.is_file():
                path = os.path.join(beginPath, item.name)
                # print('当前文件: {}'.format(path))
                size = item.stat().st_size
                filelist.append([path, size])
            else:
                # pass
                path = os.path.join(beginPath, item.name)
                # print("目录: {}".format(path))
                scanDir(path)
    except PermissionError:
        print('访问拒绝:{}'.format(beginPath))

def outPut(logPath=os.path.join(os.path.expanduser('~'),'Desktop','log.txt')):
    newlist = sorted(filelist, key=lambda x:x[1], reverse=True)
    with open(logPath,'w') as f:
        f.write("{:>6}   {}\n".format("大小","路径"))
        for file in newlist:
            f.write("{:>10} {}\n".format(formatSize(file[1]),file[0]))

def test():
    scanDir()
    outPut()


def main():
    def func(getpath):
        scanDir(getpath)
        outPut()
        print('文件搜索完成')
    def showMsg(*args):
        basePath = {"C": "C:\\", "D": "D:\\", "E": "E:\\", "F": "F:\\"}
        root.update()
        threading.Thread(target=func,args=(basePath[path.get()],)).start()
        return
    def go(*args):
        threading.Thread(target=func, args=(enter.get(),)).start()
        return
    def search(*args):
        enter.set(askdirectory())
    root = Tk()
    root.title("文件大小查看")
    path = StringVar()
    selectPath = Combobox(root, textvariable=path, values=["C","D","E","F"])
    selectPath.current(0)
    checkbtn = Button(root,text="Go",command=go)
    enter = StringVar()
    enterPath = Button(root, textvariable=enter, command=search)
    enter.set("请选择一个文件夹")
    selectPath.bind("<<ComboboxSelected>>", showMsg)
    selectPath.pack(fill=X)
    enterPath.pack(side="left")
    checkbtn.pack(fill=X)
    root.mainloop()

if __name__=="__main__":
    main()








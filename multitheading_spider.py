from threading import Thread
import queue
import requests
import re
from PIL import Image
from io import BytesIO
import os
import logging
logging.basicConfig(level=logging.WARNING)

start_url = 'http://huaban.com/favorite/anime/'
web_queue = queue.Queue()
pic_queue = queue.Queue()
check_set = set()
count = 0
if not os.path.isdir('d:\图片目录'):
    os.makedirs('d:\图片目录')


def get_links(url):
    base_url = 'http://huaban.com/pins/'
    global check_set
    r = requests.get(url)
    logging.debug('get_links:connect:{}'.format(r.status_code))
    pins_re = re.compile(r'pin_id":"?(\d*)')
    for pin in pins_re.findall(r.text):
        logging.debug('get pin:{}'.format(pin))
        if pin in check_set:
            logging.debug('pin [{}] already exist'.format(pin))
            continue
        else:
            check_set |= {pin}
            make_url = base_url + pin + '/'
            logging.debug('pic url:{}'.format(make_url))
            pic_queue.put(make_url)


def down_pic(pic_url):
    global count
    logging.warning('count: {} , pic url: {}'.format(count, pic_url))
    try:
        r = requests.get(pic_url, timeout=3)
    except requests.exceptions.ReadTimeout:
        logging.warning('连接超时')
        return
    except requests.exceptions.ConnectionError:
        logging.warning('连接错误')
        return
    logging.debug('get_pic:connect:{}'.format(r.status_code))
    html = r.text
    base_url = 'http://img.hb.aicdn.com/'
    last_url_re = re.compile(r'app\["page"\].*?"key":"(.*?)", "type":"image/(.*?)"')
    last_url, mode = last_url_re.findall(html)[0]
    logging.info('last_url:{}  mode:{}'.format(last_url, mode))
    pic_url = base_url + last_url
    pic_r = requests.get(pic_url)
    im = Image.open(BytesIO(pic_r.content))
    name = str(count) + '.' + mode
    im.save(os.path.join('d:\图片目录', name))
    count += 1


class ExtractUrlThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.name = 'extract_thread'

    def run(self):
        while True:
            web_url = web_queue.get()
            get_links(web_url)


class DownPicThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.name = 'downpic_thread'

    def run(self):
        while True:
            pic_url = pic_queue.get()
            web_queue.put(pic_url)
            down_pic(pic_url)


def main(limit=100):
    web_queue.put(start_url)
    t1 = ExtractUrlThread()
    t2 = DownPicThread()
    t1.setDaemon(True)
    t2.setDaemon(True)
    t1.start()
    t2.start()
    while True:
        if count > limit:
            return


main()

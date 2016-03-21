#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import re

root_url = 'http://pyvideo.org'
index_url = root_url + '/category/50/pycon-us-2014'


def get_video_page_urls():
    response = requests.get(index_url)
    soup = BeautifulSoup(response.text, "lxml")
    return [a.get('href') for a in soup('a', class_='thumbnail')]


def get_video_msg(video_url):
    print('url=', root_url+video_url)
    video_data = {}
    response=requests.get(root_url+video_url)
    soup=BeautifulSoup(response.text,'lxml')
    tag=soup.find(id='sidebar')
    video_data['Category'] = tag.find('a', href=re.compile('category')).string
    try:
        video_data['Speakers'] = tag.find('meta', property='author').get('content')
    except:
        video_data['Speakers'] = 'Unknown'
    video_data['Language'] = tag.find('meta', property='inLanguage').previous_element.strip()
    video_data['Recorded'] = tag.find('meta', property='dateCreated').previous_element.strip()
    try:
        video_data['Video origin'] = tag.find('a', property='embedUrl').get('href')
    except:
        video_data['Video origin'] = 'Unknown'
    # print(video_data['Category'])
    # print(video_data['Speakers'])
    # print(video_data['Language'])
    # print(video_data['Recorded'])
    # print(video_data['Video origin'])
    return video_data


def show_video_stats():
    video_list=get_video_page_urls()
    for video_url in video_list:
        print(get_video_msg(video_url))


# get_video_msg('/video/2668/writing-restful-web-services-with-flask')
show_video_stats()





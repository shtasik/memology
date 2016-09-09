# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 17:40:12 2016

@author: dmitrys
"""

###############################################################
####       Meme parsing just for lulz and science  <3      ####
###############################################################


import re
from bs4 import BeautifulSoup
from tkinter import *
import time
from dateutil import parser
import pandas as pd
import numpy as np
from urllib.request import Request, urlopen
import getpass
username = getpass.getuser()


def html_stripper(text):
    return re.sub('<[^<]+?>', '', str(text))


number_of_pages = 362
page = 1
main_url = 'http://knowyourmeme.com/'
columns = ['name', 'added', 'views', 'comments', 'status', 'year', 'tags', 'about', 'origin', 'spread']
FINAL = pd.DataFrame(columns=columns)


def getMemeUrls(page):
    req = Request('http://knowyourmeme.com/memes/all/page/{}'.format(page), headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, "lxml")
    meme_urls = soup.findAll('a', attrs={'class':'photo'})
    print('Getting all memes from page {}'.format(page))
    return meme_urls


def getAllFromPage(meme_urls):
    global FINAL
    for meme in meme_urls:
        start = time.time()
        to_append = {x:np.NaN for x in columns}
        #time.sleep(1)
        try:
            meme_url = re.split('href="|" target="|"> <img|"', str(meme))[3]
            meme_page = Request(main_url+meme_url)
            meme_page = urlopen(meme_page).read()
            meme_page = BeautifulSoup(meme_page, 'lxml')
        except:
            continue
        #### NAME & DATE
        try:
            raw = html_stripper(meme_page.find('section', attrs={'class':'info'})).split('\n')
            for i in raw:
                if i!='':
                    name = i
                    break
            for j in range(len(raw)-1):
                if raw[j] == 'Added':
                    added = raw[j+1]
            
            to_append['name'] = name
            to_append['added'] = added
        except:
            continue
        
        #### VIEWS
        try:
            views = meme_page.find('dd', attrs = {'class':'views'})
            views = re.split('title="| Views"', str(views))[1].replace(',', '')
            to_append['views'] = views
        except:
            continue
        
        #### COMMENTS
        try:
            comments = meme_page.find('dd', attrs = {'class':'comments'})
            comments = re.split('title="| Comments"', str(comments))[1]
            to_append['comments'] = comments
        except:
            continue
        
        #### PROPERTIES
        try:
            properties = meme_page.find('aside', attrs = {'class':'left'})
            properties = html_stripper(properties).split('\n')
            properties = [x for x in properties if x != '']
            
            status = properties[1]
            year = properties[3]
            tags = properties[7]
            
            to_append['status'] = status
            to_append['year'] = year
            to_append['tags'] = tags
        except:
            continue
        #### ABOUT & ORIGINS & SPREAD
        try:
            raw = html_stripper(meme_page.find('section', attrs = {'class':'bodycopy'})).split('\n')
            about, origin, spread = ('', '', '')
            for i in range(len(raw)-1):
                if raw[i] == 'About':
                    about = raw[i+1]
                elif raw[i] == 'Origin':
                    origin = raw[i+1]
                elif raw[i] == 'Spread':
                    spread = raw[i+1]
                    
            to_append['about'] = about
            to_append['origin'] = origin
            to_append['spread'] = spread
        except:
            continue
        print('got {} meme!'.format(name))
        print('elapsed time: {}'.format(time.time()-start))
        print('========')
        FINAL = FINAL.append(to_append, ignore_index=True)


for page in range(1, number_of_pages):
    getAllFromPage(getMemeUrls(page))
    

FINAL.to_csv('/Users/{}/Desktop/{}.csv'.format(username, 'Memes.csv'))
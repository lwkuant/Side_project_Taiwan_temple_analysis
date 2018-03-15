# -*- coding: utf-8 -*-
"""
Temple of Taiwan
http://www.baibai.com.tw/
"""

### Initial setup
import requests
from bs4 import BeautifulSoup
import re
import time
from collections import defaultdict

### Get the number of pages
page = requests.get('http://www.baibai.com.tw/temple.asp?Page=164&name=&keyword=&morder=')
page.encoding = 'big5'
page = BeautifulSoup(page.text)

num_pages = page.find_all('td', {"width": "55%"})[0].font.font.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text
num_pages = int(re.sub('\W', '', num_pages))

### Get the data

data_list = defaultdict(list)

#
for i in range(1, num_pages+1):
    
    start_time = time.time()
    
    ### Get web page
    page = requests.get('http://www.baibai.com.tw/temple.asp?Page=' + str(i) + '&name=&keyword=&morder=')
    page.encoding = 'big5'
    page = BeautifulSoup(page.text)
    
    num_items_per_page = int(len(page.tr.next_sibling.next_sibling.find_all('a', {"href": re.compile('^view-temple\.asp\?com_ser=')}))/3)
    
    step = int(len(page.tr.next_sibling.next_sibling.find_all('a', {"href": re.compile('^view-temple\.asp\?com_ser=')}))/num_items_per_page)
    
    ### Get data
    ## Get name of the temple
    data_list['Temple'].extend([re.search('\w.*\w', page.tr.next_sibling.next_sibling.find_all('a', {"href": re.compile('^view-temple\.asp\?com_ser=')})[x*step+0].text).group(0)\
                                                                 if 
                                re.search('\w.*\w', page.tr.next_sibling.next_sibling.find_all('a', {"href": re.compile('^view-temple\.asp\?com_ser=')})[x*step+0].text) != None else '' 
                                for x in range(num_items_per_page)])   
    
    ## Get address of the temple 
    data_list['Address'].extend([re.search('\w.*\w', page.tr.next_sibling.next_sibling.find_all('a', {"href": re.compile('^view-temple\.asp\?com_ser=')})[x*step+1].text).group(0)\
                                                                 if 
                                re.search('\w.*\w', page.tr.next_sibling.next_sibling.find_all('a', {"href": re.compile('^view-temple\.asp\?com_ser=')})[x*step+1].text) != None else '' 
                                for x in range(num_items_per_page)])   

    step = int(len(page.tr.next_sibling.next_sibling.find_all('a', {"href": re.compile('^\/temple\.asp\?keyword=')})[10:len(page.tr.next_sibling.next_sibling.find_all('a', {"href": re.compile('^\/temple\.asp\?keyword=')})) - 26])/num_items_per_page)

    ##  Get city of the temple
    data_list['City'].extend([re.search('\w.*\w', page.tr.next_sibling.next_sibling.find_all('a', {"href": re.compile('^\/temple\.asp\?keyword=')})[10:len(page.tr.next_sibling.next_sibling.find_all('a', {"href": re.compile('^\/temple\.asp\?keyword=')})) - 26][x*step+3].text).group(0)\
                                                         if 
                        re.search('\w.*\w', page.tr.next_sibling.next_sibling.find_all('a', {"href": re.compile('^\/temple\.asp\?keyword=')})[10:len(page.tr.next_sibling.next_sibling.find_all('a', {"href": re.compile('^\/temple\.asp\?keyword=')})) - 26][x*step+3].text) != None else '' 
                        for x in range(num_items_per_page)]) 
    
    ## Get God worshipped of the temple
    data_list['God'].extend([re.search('\w.*\w', page.tr.next_sibling.next_sibling.find_all('a', {"href": re.compile('^\/temple\.asp\?keyword=')})[10:len(page.tr.next_sibling.next_sibling.find_all('a', {"href": re.compile('^\/temple\.asp\?keyword=')})) - 26][x*step+1].text).group(0)\
                                                             if 
                            re.search('\w.*\w', page.tr.next_sibling.next_sibling.find_all('a', {"href": re.compile('^\/temple\.asp\?keyword=')})[10:len(page.tr.next_sibling.next_sibling.find_all('a', {"href": re.compile('^\/temple\.asp\?keyword=')})) - 26][x*step+1].text) != None else '' 
                            for x in range(num_items_per_page)]) 
    
    time.sleep(0.1)
    print('Page', i)
    print(time.time() - start_time)


import pandas as pd

df = pd.DataFrame(data_list)

import os
os.chdir('D:/Dataset/Side_project_temple_taiwan')
df.to_csv('Temple_info.csv', index = None)




from urllib import request as url_req
from bs4 import BeautifulSoup as bsp4
from core.db_conn import db_connected as db_func
import time,re


url = 'http://www.chainb.com/'

def get_html_code(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
    req = url_req.Request(url,headers=headers)
    response = url_req.urlopen(req).read().decode()
    soup = bsp4(response, 'html.parser')
    return soup



def get_news_list(html):
    news_link_list = []
    news_img_dict = {}
    for link in html:
        print('link>>>>>>>>>>>>>>>:',link,type(link))
        img = link.select('img.lazy')[0]['data-original']
        link = url + link.select('a.transition')[0]['href']
        if link in news_link_list: continue
        news_link_list.append(link)
        news_img_dict[str(link)] = str(img)

html = get_html_code(url)
# print(html)
data = html.find_all('div',{'class':'mod-art'})
print(data)
# news_link_list = []
# news_img_dict = {}
# for link in html:
#     print('link>>>>>>>>>>>>>>>:', link, type(link))
#     img = link.select('img.lazy')[0]['data-original']
#     link = url + link.select('a.transition')[0]['href']
#     if link in news_link_list: continue
#     news_link_list.append(link)
#     news_img_dict[str(link)] = str(img)



news_links, news_img_dict = get_news_list(data)

# print(news_links,news_img_dict)

# print(data,type(data))

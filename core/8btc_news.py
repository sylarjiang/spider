from urllib import request as url_req
from bs4 import BeautifulSoup as bsp4
from core.db_conn import db_connected as db_func
import time



'''
不根据栏目采集
http://www.8btc.com/blockchain              thumb-img animated flipInY
http://www.8btc.com/digital-currency        thumb animated flipInY
http://www.8btc.com/bqz                     thumb-img animated flipInY
http://www.8btc.com/vc                      thumb currency animated flipInY
http://www.8btc.com/topic                   col-md-12 col-sm-12 theme-content-header block-piece
http://www.8btc.com/week                    col-md-4 col-sm-4 topic-before week-before week-post-left
                                            col-md-6 col-sm-6 topic-now
http://www.8btc.com/bbg                     thumbnails

'''

url = 'http://www.8btc.com/'
class_name = ['article-thumbnail pull-left','article-thumbnail animated flipInY']

def get_html_code(url):
    # print(url)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
    req = url_req.Request(url,headers=headers)
    response = url_req.urlopen(req).read().decode()
    soup = bsp4(response, 'html.parser')
    return soup


def get_news_list(html,class_name=None):
    data_list = []
    for i in class_name:
        data = html.find_all('div', {'class': i})
        data_list.extend(data)
    data = html.find_all('div', {'class': 'article-thumbnail animated flipInY'})
    news_link_list = []
    news_img_dict = {}
    for link in data_list:
        if link.find('img').get('src'):
            img = link.find('img').get('src')
        else:
            img = ''
        link = link.find('a')['href']
        news_link_list.append(link)
        news_img_dict[str(link)] = str(img)
    return news_link_list,news_img_dict

def update_links(links):
    links_col= db_func(col='8btc_links')
    # links_col.delete_many({})
    today = time.strftime("%Y/%m/%d-%H:%M:%S")
    links_col.insert_one({'day': today, 'test_links': links})


def get_old_news_links():
    links_col = db_func(col='8btc_links')
    old_list = []
    for i in links_col.find({}, {'test_links': 1}): old_list.extend(i['test_links'])
    return old_list

def links_changed(news_links):
    old_links = get_old_news_links()
    news_links_all = set(news_links) | (set(old_links))
    diff_links = set(news_links) - (set(old_links))
    return diff_links,news_links_all

def http_status(link):
    import requests
    res = requests.get(link).status_code
    return int(res)


def filter_html_tags(htmlstr):
    import re
    re_comment = re.compile('<!--[^>]*-->')#HTML注释
    re_a = re.compile('<\s*a[^>]*>[^<]*<\s*/\s*a\s*>', re.I)
    re_a = re.compile('</?a[^>]*>', re.I)
    s = htmlstr.lstrip('[')
    s = s.rstrip(']')
    s = re_a.sub('', s)
    return s



def string_format(doc,format_type=''):
    word = []
    for i in doc:
        if i.string is not None:
            word.append(str(i.string.strip()))
        else:
            word.append(str(i))
    kw = '%s'%format_type.join(str(i) for i in word)
    return kw




def news_page_info(link,img=None):
    '''
    对正文页中内容处理,保留需要的信息
    :param link:
    :param img: 首页缩略图
    :return:
    '''
    print(link)
    news = {}
    news_page = get_html_code(link)

    news['news_link'] = link
    news['news_img'] = img
    if news_page.select('div.week-back') or news_page.select('div.zan-bodyer'):
        return None
    news['news_title'] = news_page.select('div.article-title > h1')[0].text.strip()
    news['news_author'] = news_page.select('span.author-name')[0].text.strip()
    news['news_time'] = news_page.select('time')[0].text.strip()
    news['news_keyword'] = ''
    if news_page.find('div', {'class': 'content-source-info'}) is True:
        news['news_source'] = news_page.find('div', {'class': 'content-source-info'}).get_text()
    else:
        news['news_source'] = '8btc'
    news['news_synopsis'] = ''
    news_content_code = news_page.find('div', {'class': 'article-content'})
    news_content = news_content_code.find('div', {'class': 'content-bottom'}).extract()
    if news_content_code.find('div', {'class': 'ad akp-adv'}) is True:
        news_content = news_content_code.find('div', {'class': 'ad akp-adv'}).extract()
    if news_content_code.find('div', {'class': 'content-source-info'}) is True:
        news_content = news_content_code.find('div', {'class': 'content-source-info'}).extract()
    news['news_content'] = filter_html_tags(string_format(news_content_code))
    news['status'] = '0'
    news['scan_count'] = 0
    news['category_id'] = ''
    return news



def update_news_info(links,img_dict):
    for link in links:
        link_status = http_status(link)
        if link_status < 400:
            if link in img_dict.keys():
                news_img = img_dict[link]
            else:
                news_img = ''
            news = news_page_info(link, news_img)
            if news is not None:
                col = db_func(col='news_content')
                col.insert_one(news)





html = get_html_code(url)
news_links, news_img_dict = get_news_list(html,class_name)
news_links = list(set(news_links))

diff_links,news_links_all = links_changed(news_links)
if len(news_links_all) > 0:
    update_links(list(news_links_all))
    update_news_info(news_links_all,news_img_dict)












# news_img_dict={}
# # link = 'http://www.8btc.com/binance-incubator'
# link = 'http://www.8btc.com/coinweek-204#week-5'
# news_img_dict[link] = 'http://cdn.8btc.com/wp-content/uploads/2018/07/201807160909261536-380x152.jpg'
# link_status = http_status(link)
# news = {}
# news_page = get_html_code(link)
# if news_page.select('div.week-back'):
#
#     exit()
# news['news_title'] = news_page.select('div.article-title > h1')[0].text.strip()
# news['news_author'] = news_page.select('span.author-name')[0].text.strip()
# news['news_time'] = news_page.select('time')[0].text.strip()
# news['news_keyword'] = ''
# if news_page.find('div',{'class':'content-source-info'}) is True:
#     news['news_source'] = news_page.find('div',{'class':'content-source-info'}).get_text()
# else:
#     news['news_source'] = '8btc'
# news['news_synopsis'] = ''
# news_content_code = news_page.find('div', {'class': 'article-content'})
# news_content = news_content_code.find('div',{'class' : 'content-bottom'}).extract()
# if news_content_code.find('div',{'class' : 'ad akp-adv'}) is True:
#     news_content = news_content_code.find('div',{'class' : 'ad akp-adv'}).extract()
# if news_content_code.find('div',{'class' : 'content-source-info'}) is True:
#     news_content = news_content_code.find('div',{'class' : 'content-source-info'}).extract()
# news['news_content'] = filter_html_tags(string_format(news_content_code))
# news['status'] = '0'
# news['scan_count'] = 0
# news['category_id'] = ''
# # news['news_content'] = news_page.find('div', {'class': 'article-content'})
# print(type(news_content_code))
# # news['news_author'] = news_page.select('div.single-crumbs clearfix > span > a')[0].text.strip()
# print(news_content_code)










'''
首页采集目标
大图:
links   http://www.8btc.com/coinweek-202
http://cdn.8btc.com/wp-content/uploads/2018/07/201807160909261536-380x152.jpg

zan-thumbnail animated flipInY > a :href > img :src
article-thumbnail pull-left  > a :href > div > img : src
article-thumbnail animated flipInY > a :href > div > img : src

'''





















from urllib import request as url_req
from bs4 import BeautifulSoup as bsp4
from core.db_conn import db_connected as db_func
import time,sys,re



url = "https://www.leiphone.com/"
drop_link = 'https://www.leiphone.com/latest/index/id/4149'


def filter_html_tags(htmlstr):
    re_comment = re.compile('<!--[^>]*-->')
    s = htmlstr.lstrip('[')
    s = s.rstrip(']')
    s = re_comment.sub('',s)
    return s

# 字符拼接
def string_format(doc,format_type=''):
    word = []
    for i in doc:
        if i.string is not None:
            word.append(str(i.string.strip()))
        else:
            word.append(str(i))

    kw = '%s'%format_type.join(str(i) for i in word)
    return kw


def get_html_code(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
    req = url_req.Request(url,headers=headers)
    response = url_req.urlopen(req).read().decode()
    soup = bsp4(response, 'html.parser')
    return soup


def get_news_list(html):
    # data = html.find_all('div',{'class':'box'})
    news_link_list = []
    news_img_dict = {}
    for link in html:
        if len(link.select('div.img')) > 0:
            img = link.find_all('a')[1].find('img')['src']
            link = link.find_all('a')[1]['href']
        elif link.select('div.box2'):
            continue
        else:
            img = link.find_all('a')[0].find('img')['src']
            link = link.find_all('a')[0]['href']
        if link in news_link_list:continue
        news_link_list.append(link)
        news_img_dict[str(link)] = str(img)
    return news_link_list,news_img_dict

#
def news_page_info(link,img=None):
    print(link)
    news = {}
    news_page = get_html_code(link)
    news['news_link'] = link
    news['news_img'] = img
    if news_page.select('div.article-title > div.inner > h1') is False:
        print('1111')
        return {}
    news['news_title'] = news_page.select('div.article-title > div.inner > h1')[0].text.strip()
    news['news_author'] = news_page.select('td.aut > a')[0].text.strip()
    news['news_time'] = news_page.select('td.time')[0].text.strip()
    news['news_keyword'] = ''
    news['news_source'] = 'www.leiphone.com'
    news['news_synopsis'] = news_page.select('div.article-lead')[0].text.strip()
    news_content_code = news_page.find('div', {'class': 'lph-article-comView'})
    news_content = string_format(news_content_code)
    news['news_content'] = filter_html_tags(str(news_content))
    news['status'] = '0'
    news['scan_count'] = 0
    news['category_id'] = ''
    return news


def get_old_news_links():
    links_col = db_func(col = 'leiphone_links')
    old_list = []
    for i in links_col.find({}, {'news_links': 1}): old_list.extend(i['news_links'])
    return old_list

def links_changed(news_links):
    old_links = get_old_news_links()

    news_links_all = set(news_links) | (set(old_links))

    diff_links = set(news_links) - (set(old_links))
    return diff_links,news_links_all

def update_links(links):
    links_col= db_func(col = 'leiphone_links')
    links_col.delete_many({})
    today = time.strftime("%Y/%m/%d-%H:%M:%S")
    links_col.insert_one({'day': today, 'news_links': links})

def http_status(link):
    import requests
    res = requests.get(link).status_code
    return int(res)


def update_news_info(links,img_dict):
    col = db_func(col='news_content_lei')
    col.delete_many({})           #清空表重新生成newsinfo
    i = 0
    count = 3
    for link in links:
        print(link)
        link_status = http_status(link)
        if link_status < 400:
            if link in img_dict.keys():
                news_img = img_dict[link]
            else:
                news_img = ''
            news = news_page_info(link, news_img)
            col = db_func(col = 'news_content_lei')
            col.insert_one(news)
            i += 1
            if i > count:
                time.sleep(120)
                count = count + 3




html = get_html_code(url)
data = html.select('li > div.box')
news_links, news_img_dict = get_news_list(data)
news_links = set(news_links)
if drop_link in news_links:
    news_links.remove(drop_link)
print(news_links)
news_links = set(news_links)
diff_links,news_links_all = links_changed(news_links)
if drop_link in news_links_all:
    news_links_all.remove(drop_link)
if len(news_links_all) > 0:
    update_links(list(news_links_all))
    update_news_info(news_links_all,news_img_dict)
print(len(diff_links))






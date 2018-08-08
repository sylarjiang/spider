from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup as bsp4
from core.db_conn import db_connected as db_func


url = ['http://www.8btc.com/blockchain','http://www.8btc.com/bitcoin/page/']

def get_html_code(url,link_type=None):
    chrome_option = Options()
    chrome_option.add_argument('--headless')
    chrome_option.add_argument('--disable-gpu')
    browserdrive = 'D:/git/spider/core/chromedriver.exe'
    driver = webdriver.Chrome(executable_path=browserdrive,chrome_options=chrome_option)
    # driver = webdriver.Chrome(executable_path=browserdrive)
    driver.get(url)

    if link_type == 'blockchain':
    # if driver.find_element_by_id('load_more_list').click():
        for i in range(3):
            driver.find_element_by_id('load_more_list').click()
            time.sleep(3)
    if link_type == 'bitcoin':
        pass
    web_code = driver.page_source
    html = bsp4(web_code,'html.parser')
    return html

def get_news_list(html):
    data = html.find_all('div', class_ = ['thumb-img','animated','flipInY'])
    news_link_list = []
    news_img_dict = {}
    for link in data:
        # print(link)
        if link.find('img').get('data-original'):
            img = link.find('img').get('data-original')
        elif link.find('img').get('src'):
            img = link.find('img').get('src')
        else:
            img = ''
        link = link.find_all('a')[0]['href'].strip()
        if link in news_link_list: continue
        news_link_list.append(link)
        news_img_dict[link] = img.strip()

        time.sleep(1)
    return news_link_list,news_img_dict


def update_links(links):
    links_col= db_func(col='8btc_links')
    # links_col.delete_many({})
    today = time.strftime("%Y/%m/%d-%H:%M:%S")

    links_col.insert_one({'day': today, 'news_links': links})

def get_old_news_links():
    links_col = db_func(col='8btc_links')
    old_list = []
    for i in links_col.find({}, {'news_links': 1}):
        old_list.extend(i['news_links'])
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

def string_format(doc,format_type=''):
    word = []
    for i in doc:
        if i.string is not None:
            word.append(str(i.string.strip()))
        else:
            word.append(str(i))
    kw = '%s'%format_type.join(str(i) for i in word)
    return kw

def filter_html_tags(htmlstr):
    import re
    re_comment = re.compile('<!--[^>]*-->')#HTML注释
    re_a = re.compile('<\s*a[^>]*>[^<]*<\s*/\s*a\s*>', re.I)
    re_a = re.compile('</?a[^>]*>', re.I)
    s = htmlstr.lstrip('[')
    s = s.rstrip(']')
    s = re_a.sub('', s)
    return s

def news_page_info(link,img=None):
    print(link)
    news = {}
    news_page = get_html_code(link, 'news_info')

    news['news_link'] = link
    news['news_img'] = img
    # if news_page.select('div.week-back') or news_page.select('div.zan-bodyer'):
    #     # return None
    #     pass
    # if news_page.select('div.article-title > h1'):

    if news_page.find('div', {'class': 'article-title'}):
        # news['news_title'] = news_page.select('div.article-title > h1')[0].text.strip()
        news['news_title'] = news_page.find('div', {'class': 'article-title'}).get_text().strip()

    # if news_page.select('article-content-title-box > div.title') is True:
    #     print('2222')
    #     news['news_title'] = news_page.select('article-content-title-box > div.title')[0].text.strip()

    if news_page.find('div', {'class': 'single-crumbs'}):
        news['news_author'] = news_page.find('div', {'class': 'single-crumbs'}).find('a').get_text().strip()

        # news['news_author']  = news_page.select('span.author-name')[0].text.strip()

    # if news_page.select('a.author-a1') is True:
    #     print(news_page.select('a.author-a1'))
    # news['news_author'] = news_page.select('span.author-name')[0].text.strip()
    if news_page.find('time'):
        news['news_time'] = news_page.find('time').get_text().strip()

    # news['news_time'] = news_page.select('time')[0].text.strip()

    news['news_keyword'] = ''
    if news_page.find('div', {'class': 'content-source-info'}) is True:
        news['news_source'] = news_page.find('div', {'class': 'content-source-info'}).get_text()
    else:
        news['news_source'] = '巴比特'
    news['news_synopsis'] = ''
    news_content_code = news_page.find('div', {'class': 'article-content'})
    if news_content_code.find('div', {'class': 'content-bottom'}):
        news_content = news_content_code.find('div', {'class': 'content-bottom'}).extract()
    if news_content_code.find('div', {'class': 'akp-adv'}):
        news_content = news_content_code.find('div', {'class': 'akp-adv'}).extract()
    if news_content_code.find('div', {'class': 'content-source-info'}):
        news_content = news_content_code.find('div', {'class': 'content-source-info'}).extract()

    news['news_content'] = str(filter_html_tags(string_format(news_content_code)))
    news['status'] = '0'
    news['scan_count'] = 0
    news['category_id'] = ''
    return news

def update_news_info(links,news_img_dict):
    for link in links:
        link_status = http_status(link)
        if link_status < 400:
            if link in news_img_dict.keys():
                news_img = news_img_dict[link]
            else:
                news_img = ''
            news = news_page_info(link, news_img)

        if news is not None:
            col = db_func(col='8btc_news_content')
            col.insert_one(news)



for addr in url:
    if addr == 'http://www.8btc.com/blockchain':
        # blockchain

        html = get_html_code(addr,link_type='blockchain')
        news_links, news_img_dict = get_news_list(html)
        diff_links,news_links_all = links_changed(news_links)
        print(diff_links,news_img_dict)
        if len(diff_links) > 0:
            update_links(list(diff_links))
            update_news_info(diff_links,news_img_dict)

    elif addr == 'http://www.8btc.com/bitcoin/page/':
        # bitcoin
        news_links = []
        news_img_dict = {}
        for i in range(1,4):
            page = addr+str(i)
            html = get_html_code(page,'bitcoin')
            page_links,page_img_dict = get_news_list(html)
            news_links.extend(page_links)
            news_img_dict.update(page_img_dict)
        diff_links,news_links_all = links_changed(news_links)
        print(diff_links,news_img_dict)
        if len(diff_links) > 0:
            update_links(list(diff_links))
            update_news_info(diff_links,news_img_dict)
    else:
        print('url wrong')



# print(len(news_links_all))


# link = 'http://www.8btc.com/thomson-reuters-50crypto'
# news = news_page_info(link)
# print(news,type(news))
# col = db_func(col='news_content_8btc')
# col.insert_one(news)

# def update_news_info
# for link in news_links_all:
#     link_status = http_status(link)
#     if link_status < 400:
#         if link in news_img_dict.keys():
#             news_img = news_img_dict[link]
#         else:
#             news_img = ''
#         news = news_page_info(link, news_img)
#
#     if news is not None:
#         col = db_func(col='8btc_news_content')
#         col.insert_one(news)




'''

def #news_page_info
print(link)
news = {}
news_page = get_html_code(link,'news_info')

news['news_link'] = link
news['news_img'] = ''
# if news_page.select('div.week-back') or news_page.select('div.zan-bodyer'):
#     # return None
#     pass
# if news_page.select('div.article-title > h1'):

if news_page.find('div',{'class':'article-title'}):
    # news['news_title'] = news_page.select('div.article-title > h1')[0].text.strip()
    news['news_title'] = news_page.find('div',{'class':'article-title'}).get_text().strip()

# if news_page.select('article-content-title-box > div.title') is True:
#     print('2222')
#     news['news_title'] = news_page.select('article-content-title-box > div.title')[0].text.strip()

if news_page.find('div', {'class' : 'single-crumbs'}):
    news['news_author'] = news_page.find('div', {'class' : 'single-crumbs'}).find('a').get_text().strip()

    # news['news_author']  = news_page.select('span.author-name')[0].text.strip()


# if news_page.select('a.author-a1') is True:
#     print(news_page.select('a.author-a1'))
# news['news_author'] = news_page.select('span.author-name')[0].text.strip()

news['news_time'] = news_page.find('time').get_text().strip()

# news['news_time'] = news_page.select('time')[0].text.strip()

news['news_keyword'] = ''
if news_page.find('div', {'class': 'content-source-info'}) is True:
    news['news_source'] = news_page.find('div', {'class': 'content-source-info'}).get_text()
else:
    news['news_source'] = '8btc'
news['news_synopsis'] = ''
news_content_code = news_page.find('div', {'class': 'article-content'})
if news_content_code.find('div', {'class': 'content-bottom'}):
    news_content = news_content_code.find('div', {'class': 'content-bottom'}).extract()

if news_content_code.find('div', {'class': 'akp-adv'}):
    news_content = news_content_code.find('div', {'class': 'ad akp-adv'}).extract()
# if news_content_code.find('div', {'class': 'content-source-info'}) is True:
#     news_content = news_content_code.find('div', {'class': 'content-source-info'}).extract()
print(news_content_code,type(news_content_code))
# news['news_content'] = filter_html_tags(string_format(news_content_code))
news['news_content'] = news_content_code
news['status'] = '0'
news['scan_count'] = 0
news['category_id'] = ''
print(news)
# print(news_content)
'''








# update_links(news_links)


# driver.find_element_by_link_text('加载更多').click()




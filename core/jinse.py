from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup as bsp4
from bs4 import Comment
from core.db_conn import db_connected as db_func



url = 'https://www.jinse.com/'

def get_html_code(url,link_type=None):
    chrome_option = Options()
    chrome_option.add_argument('--headless')
    chrome_option.add_argument('--disable-gpu')
    browserdrive = 'D:/git/spider/core/chromedriver.exe'
    driver = webdriver.Chrome(executable_path=browserdrive,chrome_options=chrome_option)
    # driver = webdriver.Chrome(executable_path=browserdrive)
    driver.get(url)

    if link_type == None:
        for i in range(5):
            # driver.find_element_by_id('custom-click-loade').click()
            driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            time.sleep(3)
    web_code = driver.page_source
    html = bsp4(web_code, 'html.parser')
    return html


def get_news_list(html):
    data = html.find_all('ol', class_=['clear', 'list'])
    news_link_list = []
    news_img_dict = {}
    for link_code in data:
        if link_code.find('a', class_='article-img'):
            link_code = link_code.find('a', class_='article-img')
        else:continue
        if link_code.find('img'):
            img = link_code.find('img').get('src').strip()
        else:
            img = ''
        if link_code['href']:
            link = link_code['href'].strip()
        if link in news_link_list: continue
        if link.startswith('http') is False: continue
        news_link_list.append(link)
        news_img_dict[link] = img
    return news_link_list, news_img_dict


def get_old_news_links():
    col = db_func(col='js_news_content')
    old_list = []
    for i in col.find({}, {'news_link': 1}):
        if i['news_link'].find('jinse'):
            old_list.append(i['news_link'])
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
    re_a = re.compile('</?a[^>]*>', re.I)
    s = htmlstr.lstrip('[')
    s = s.rstrip(']')
    s = re_a.sub('', s)
    return s

def string_format(doc,format_type=''):
    word = []
    for i in doc:
        if i.string is not None:
            word.append(str(i.string).strip())
        else:
            word.append(str(i).strip())
    kw = '%s'%format_type.join(str(i) for i in word)
    return kw

def news_page_info(link,img=''):

    news = {}
    news_page = get_html_code(link, 'news_info')
    today = time.strftime("%Y/%m/%d-%H:%M:%S")
    news['spider_time'] = today
    news['news_link'] = link
    news['news_img'] = img
    if news_page.find('h2'):
        news['news_title'] = news_page.find('h2').get_text().strip()

    if news_page.find('div', class_='article-info').find('a'):
        news['news_author'] = news_page.find('div', class_='article-info').find('a').get_text().strip()

    if news_page.find('div', class_='time'):
        news['news_time'] = news_page.find('div', class_='time').get_text().strip()

    news['news_keyword'] = ''
    news['news_source'] = '金色财经'
    news['news_synopsis'] = ''

    if news_page.find('div', class_=['js-article-detail']):
        news_content_code = news_page.find('div', class_=['js-article-detail'])

    for i in news_content_code(text=lambda text: isinstance(text, Comment)):
        i.extract()

    news['news_content'] = str(filter_html_tags(string_format(news_content_code)))
    news['status'] = '0'
    news['scan_count'] = 0
    news['category_id'] = ''
    return news

def update_news_info(links,news_img_dict):
    for link in links:
        news = None
        link_status = http_status(link)
        if link_status < 400:
            if link in news_img_dict.keys():
                news_img = news_img_dict[link]
            else:
                news_img = ''
            news = news_page_info(link, news_img)

            if news is not None:
                col = db_func(col='js_news_content')
                col.insert_one(news)

html = get_html_code(url)
news_link_list, news_img_dict = get_news_list(html)
diff_links,news_links_all = links_changed(news_link_list)


if len(diff_links) > 0:
    update_news_info(diff_links, news_img_dict)






























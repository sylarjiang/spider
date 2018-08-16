from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup as bsp4
from bs4 import Comment
from core.db_conn import db_connected as db_func



url = 'http://www.chaindd.com'


def get_html_code(url,link_type=None):
    chrome_option = Options()
    chrome_option.add_argument('--headless')
    chrome_option.add_argument('--disable-gpu')
    chrome_option.add_argument('--no-sandbox')
    # winconf
    # browserdrive = 'D:/git/spider/core/chromedriver.exe'
    # driver = webdriver.Chrome(executable_path=browserdrive)
    # linux
    browserdrive = '/usr/bin/chromedriver'
    driver = webdriver.Chrome(executable_path=browserdrive,chrome_options=chrome_option)
    driver.get(url)

    if link_type == None:
        for i in range(5):
            driver.find_element_by_class_name('load_more').click()
            time.sleep(3)
    web_code = driver.page_source
    html = bsp4(web_code, 'html.parser')
    driver.quit()
    return html


def get_news_list(html):
    data = html.find_all('li', class_=['post_part'])
    news_link_list = []
    news_img_dict = {}
    for link in data:
        if link.find('img').get('src'):
            img = link.find('img').get('src')
        else:
            img = ''
        link = link.find_all('a')[0]['href'].strip()
        if link in news_link_list: continue
        link = url+link
        news_link_list.append(link)
        news_img_dict[link] = img.strip()
    return news_link_list, news_img_dict


def get_old_news_links():
    col = db_func(col='news_content')
    old_list = []
    for i in col.find({}, {'news_link': 1}):
        if i['news_link'].find('chaindd'):
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
    print(link)
    news = {}
    news_page = get_html_code(link, 'news_info')
    today = time.strftime("%Y/%m/%d-%H:%M:%S")
    news['spider_time'] = today
    news['news_link'] = link
    news['news_img'] = img
    if news_page.find('h1'):
        news['news_title'] = news_page.find('h1').get_text().strip()

    if news_page.find('div', class_=['author-cont', 'f1']):
        news['news_author'] = news_page.find('div', class_=['author-cont', 'f1']).find('a').get_text().strip()

    if news_page.find('span', class_='time'):
        news['news_time'] = news_page.find('span', class_='time').get_text().strip()

    news['news_keyword'] = ''
    news['news_source'] = '链得得'

    if news_page.find('p', class_='post-abstract'):
        news['news_synopsis'] = news_page.find('p', class_='post-abstract').get_text().strip()
    if news_page.find('article').find('div', class_='inner'):
        news_content_code = news_page.find('article').find('div', class_='inner')

    for i in news_content_code(text=lambda text: isinstance(text, Comment)):
        i.extract()

    news['news_content'] = str(filter_html_tags(string_format(news_content_code)))
    news['status'] = '0'
    news['scan_count'] = 0
    news['category_id'] = ''
    from hashlib import md5
    news['news_md5'] = str(md5(news['news_content'].encode()).hexdigest())

    return news


def update_news_info(links,news_img_dict):
    for link in links:
        news = None
        if link in news_img_dict.keys():
            news_img = news_img_dict[link]
        else:
            news_img = ''
        news = news_page_info(link, news_img)

        if news is not None:
            col = db_func(col='news_content')
            col.insert_one(news)


def main():
    html = get_html_code(url)
    news_link_list, news_img_dict = get_news_list(html)
    diff_links,news_links_all = links_changed(news_link_list)
    if len(diff_links) > 0:
        print(diff_links)
        update_news_info(diff_links, news_img_dict)

if __name__ == '__main__':
    main()





























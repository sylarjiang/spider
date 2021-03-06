from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import random
from bs4 import BeautifulSoup as bsp4
from bs4 import Comment
from core.db_conn import db_connected as db_func
from conf import config



url = 'https://www.8btc.com/news'

def get_html_code(url,link_type=None):
    chrome_option = Options()
    chrome_option.add_argument('--headless')
    chrome_option.add_argument('--disable-gpu')
    chrome_option.add_argument('--no-sandbox')

    browserdrive = config.browserdrive
    # driver = webdriver.Chrome(executable_path=browserdrive)
    driver = webdriver.Chrome(executable_path=browserdrive,chrome_options=chrome_option)

    driver.get(url)

    if link_type == None:
        for i in range(5):
            driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            time.sleep(3)
    web_code = driver.page_source
    html = bsp4(web_code, 'html.parser')
    driver.quit()
    return html


def get_news_list(html):
    web_addr = 'https://www.8btc.com'
    data = html.find_all('div', class_ = 'article-item__thumb')
    news_link_list = []
    news_img_dict = {}
    for link in data:
        # print(link)
        if link.find('img').get('data-src'):
            img = link.find('img').get('data-src')
        elif link.find('img').get('src'):
            img = link.find('img').get('src')
        else:
            img = ''
        link = link.find_all('a')[0]['href'].strip()
        if link in news_link_list: continue
        link  = web_addr + link
        news_link_list.append(link)
        news_img_dict[link] = img.strip()
        time.sleep(1)
    return news_link_list, news_img_dict


def get_old_news_md5(news_md5):
    col = db_func(col='news_content')
    for i in col.find({}, {'news_md5': 1}):
        if 'news_md5' in i.keys():
            if news_md5 == i['news_md5'] :
                return True
    return False


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
    today = time.strftime("%Y-%m-%d %H:%M:%S")
    news['spider_time'] = today
    news['news_link'] = link

    from core.tool_func import check_url
    img = check_url(img)
    news['news_img'] = img

    if news_page.find('h1'):
        news['news_title'] = news_page.find('h1').get_text().strip()

    if news_page.find('span', {'class': 'header__info-item'}):
        if news_page.find('span', {'class': 'header__info-item'}).find('a'):
            news['news_author'] = news_page.find('span', {'class': 'header__info-item'}).find('a').get_text().strip()

    news['news_time']= time.strftime("%Y-%m-%d")

    news['news_keyword'] = ''
    news['news_source'] = 'www.8btc.com'
    news['news_synopsis'] = ''

    if news_page.find('div', {'class': 'bbt-html'}):
        status = '1'
        news_content_code = news_page.find('div', {'class': 'bbt-html'})
        for i in news_content_code(text=lambda text: isinstance(text, Comment)):
            i.extract()
    else:
        news_content_code = ''
        status = '0'

    news['news_content'] = str(filter_html_tags(string_format(news_content_code)))
    if news['news_content'] == '' or news['news_title'] == '':
        news = None
        return news
    news['status'] = status
    news['scan_count'] = random.randint(50,100)
    news['category_id'] = config.category_id
    from hashlib import md5
    news['news_md5'] = str(md5(news['news_content'].encode()).hexdigest())
    return news


def update_news_info(links,news_img_dict):
    for link in links:
        news = None
        # link_status = http_status(link)
        # if link_status < 400:
        if link in news_img_dict.keys():
            news_img = news_img_dict[link]
        else:
            news_img = ''
        news = news_page_info(link, news_img)
        md5_checked = get_old_news_md5(news['news_md5'])
        if md5_checked is True:
            continue
        if news is not None:
            col = db_func(col='news_content')
            col.insert_one(news)


def main():
    html = get_html_code(url)
    news_links, news_img_dict = get_news_list(html)
    print('8btc>>>>>: ',news_links)
    if len(news_links) > 0:
        update_news_info(news_links,news_img_dict)



if __name__ == '__main__':
    main()
























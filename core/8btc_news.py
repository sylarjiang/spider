from urllib import request as url_req
from bs4 import BeautifulSoup as bsp4
from core.db_conn import db_connected as db_func
import time


url = 'http://www.8btc.com/'

def get_html_code(url):
    '''
    伪装浏览器，将获取的页面使用beautifulsoup进行分析
    :param url: 需要分析的页面url
    :return: 返回soup对象
    '''
    # print(url)          #打印地址,查看哪个链接报错
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
    req = url_req.Request(url,headers=headers)
    response = url_req.urlopen(req).read().decode()
    soup = bsp4(response, 'html.parser')
    return soup


def get_news_list(html):
    '''
    新闻链接地址
    将一个页面中的指定类型链接提取出来.通常为新闻的正文页地址和图片
    :param html: soup对象
    :return: 返回字典 key为图片，val为地址
    '''
    data = html.find_all('div', {'class': 'article-thumbnail animated flipInY'})
    news_link_list = []
    news_img_dict = {}
    for link in data:

        img = link.find('img').get('src')
        link = link.find('a')['href']


        news_link_list.append(link)
        news_img_dict[str(link)] = str(img)
    return news_link_list,news_img_dict




html = get_html_code(url)
# print(html)
news_links, news_img_dict = get_news_list(html)
print(len(news_img_dict))

data = html.find_all('div', {'class': 'article-thumbnail animated flipInY'})
# print(data[0].find('img').get('src'),type(data[0].find('img')))
# news_link_list = []
# news_img_dict = {}
# for link in data:
#     link = link.find('a')['href']
#     print(link)
#     img = link.find('img')
#     news_link_list.append(link)
#     news_img_dict[str(link)] = str(img)


# news_links, news_img_dict=get_news_list(html)







'''

大图:
links
article-thumbnail animated flipInY
href img


普通
links: 
article-thumbnail pull-left >a 

image
article-thumbnail pull-left > div class(动态) >image


'''





















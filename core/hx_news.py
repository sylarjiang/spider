from urllib import request as url_req
from bs4 import BeautifulSoup as bsp4

url = "http://www.huoxing24.com/"

# 获取页面源代码
def get_html_code(url):
    # print(url)          #打印地址,查看哪个链接报错
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
    req = url_req.Request(url,headers=headers)
    response = url_req.urlopen(req).read().decode()
    html = bsp4(response, 'html.parser')
    return html

# 获取首页新闻列表,# 新闻链接地址
def get_news_list(html):
    data = html.find_all('div',{'class':'index-news-list'})
    news_link_list = []
    for link in data:
        link = link.find_all('a')[0]['href']
        news_link_list.append(link)
    return news_link_list

# 获取新闻内容,并处理需要的信息
def news_page_info(link):
    news = {}
    news_page = get_html_code(link)
    news['news_link'] = link
    news_issue = news_page.find('div', {'class': 'text-header'})
    # print(news_issue.find('p', {'class': 'time'}))
    news['news_title'] = news_page.title.string
    news['news_author'] = news_issue.find('p', {'class': 'author'}).find('a').attrs['title']
    news['news_time'] = news_issue.find('p', {'class': 'time'}).find('span').string.strip()
    keyword = news_issue.find('p', {'class': 'keyword'}).find_all('a')
    word = []
    for i in keyword:
        if i.string is not None:
            word.append(str(i.string))
    kw = ','.join(str(i) for i in word)
    news['news_keyword'] = kw
    news['news_source'] = news_page.find('div', {'class': 'source-text'}).find('p').find('span').string.strip()
    news['news_synopsis'] = news_page.find('div', {'class': 'details-synopsis active'}).find('h2').string.strip()

    news_content_code = news_page.find('div', {'class': 'detail-text-cont simditor-body'})
    # print(news_content_code)
    if 'find_all' in dir(news_content_code.find('div')):
        news_content = news_content_code.find('div').find_all('p')
    else:
        news_content = news_content_code
    news['news_content'] = news_content
    # news['news_content'] = news_page.find('div', {'class': 'detail-text-cont simditor-body'}) #content多和少一个标签
    # news['news_content'] = news_page.find('div', {'class': 'detail-text-cont simditor-body'}).find('div').find_all('p')
    return news

all_news = []
html = get_html_code(url)
news_list = get_news_list(html)

# for link in news_list:
#     news = news_page_info(link)
#     all_news.append(news_page_info(link))
#
# print(all_news)

news = news_page_info('http://www.huoxing24.com/newsdetail/2018072212013055976.html')
print(news)


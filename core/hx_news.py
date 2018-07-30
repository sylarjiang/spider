from urllib import request as url_req
from bs4 import BeautifulSoup as bsp4
from core.db_conn import db_connected as db_func

import datetime

url = "http://www.huoxing24.com/"


# 字符过滤
def filter_html_tags(htmlstr):
    '''
    清洗html文本中的指定标签，优化目标，动态载入过滤目标
    大部分过滤注释
    :param htmlstr: 包含html标签的字符文本
    :return: 过滤后的字符文本
    '''
    import re
    #先过滤CDATA
    # re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>',re.I) #匹配CDATA
    # re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)#Script
    # re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)#style
    # re_br = re.compile('<br\s*?/?>')#处理换行
    # re_p = re.compile('</?[^(img)]+[^>]*>') #除了img标签意外的html标签都删除
    re_comment = re.compile('<!--[^>]*-->')#HTML注释

    # s = re_cdata.sub('', htmlstr)#去掉CDATA
    # s = re_script.sub('', s) #去掉SCRIPT
    # s = re_style.sub('', s)#去掉style
    # s = re_br.sub('\n', s)#将br转换为换行
    # s = re_p.sub('', s) #去掉HTML 标签
    # s = re_comment.sub('', s)
    # blank_line = re.compile('\n+')
    # s = blank_line.sub('\n',s)
    s = htmlstr.lstrip('[')
    s = s.rstrip(']')
    return s

# 字符拼接
def string_format(doc,format_type=''):
    '''
    拼接字符串
    :param doc: 需要过滤的文本
    :param format_type: 格式化连接时加入的分割符默认不加
    :return:
    '''
    word = []
    for i in doc:
        if i.string is not None:
            word.append(str(i.string.strip()))
        else:
            word.append(str(i))

    kw = '%s'%format_type.join(str(i) for i in word)
    return kw


# 获取页面源代码
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

# 新闻链接地址
def get_news_list(html):
    '''
    将一个页面中的指定类型链接提取出来.通常为新闻的正文页地址
    :param html: soup对象
    :return: 返回一个网址列表
    '''
    data = html.find_all('div',{'class':'index-news-list'})
    news_link_list = []
    for link in data:
        link = link.find_all('a')[0]['href']
        news_link_list.append(link)
    return news_link_list

# 对正文页中内容处理,保留需要的信息
def news_page_info(link):
    news = {}
    news_page = get_html_code(link)
    news['news_link'] = link
    news['news_title'] = news_page.title.string
    news['news_author'] = news_page.select('div.issue-box > p.author > a')[0].text.strip()
    news['news_time'] = news_page.select('div.issue-box > p.time > span')[0].text.strip()
    news['news_keyword'] = string_format(news_page.find('div', {'class': 'text-header'}).find('p', {'class': 'keyword'}).find_all('a'),',')

    news['news_source'] = news_page.find('div', {'class': 'source-text'}).find('p').find('span').string.strip()
    news['news_synopsis'] = news_page.find('div', {'class': 'details-synopsis active'}).find('h2').string.strip()

    news_content_code = news_page.find('div', {'class': 'detail-text-cont simditor-body'})
    # if 'find_all' in dir(news_content_code.find('div')): # 需要去掉div时,针对两种div判断选取内容
    #     news_content = news_content_code.find('div').find_all('p')
    # else:
    #     news_content = news_content_code
    news_content = string_format(news_content_code)
    news['news_content'] = filter_html_tags(str(news_content))
    news['news_published'] = 0
    return news



html = get_html_code(url)
news_list = get_news_list(html)
news_list = list(set(news_list))    # 这一步是去除掉重复的链接

def update_news_content(news_list):
    '''
    传入一个链接列表,存储到mongodb
    :param news_list:
    :return:
    '''
    col = db_func(col='hx_news')
    # col.delete_many({})
    # 新闻列表页,收集link并处理正文
    for link in news_list:
        news = news_page_info(link)
        col = db_func(col='hx_news')
        col.insert_one(news)


# # 指定正文页测试
# url = 'http://www.huoxing24.com/newsdetail/20180724104534392494.html'
# news = news_page_info(url)
# print(news)




# # 数据库相关操作
links_col = db_func(col='news_links')
old_news_links = links_col.find({},{'_id':0})
old_list = []
for i in links_col.find():old_list.extend(i['new_links'])
print(old_list)

# 删除所有链接并重新保存一份
# links_col.delete_many({})
# links_col.insert_one({'_id':'news_links','new_links':news_list})


# links_col.insert_one({'news_links':news_list})    #所有链接存为一个条目
# for i in  links_col.find():                         #取链接
#     print(type(i['news_links']),len(set(i['news_links'])))

# x= links_col.find()                                  #查网址列表的key
# for k in x:
#     print(k.keys())

# for k,v in enumerate(news_list,1):                #每个网址单独存一个条目
#     key = 'link_addr%s'%k
#     res={key: str(v)}
#     links_col.insert_one(res)


# col = db_func(col='hx_news')
# myquery = {'news_title': { '$regex': '^EOS'}}   #查询所有标题以EOS开始的新闻
# for i in col.find(myquery): print(i['news_link'])





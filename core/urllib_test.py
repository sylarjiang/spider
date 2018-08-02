
from urllib import request as url_req
from bs4 import BeautifulSoup as bsp4

url = 'http://www.8btc.com/'
class_name = ['article-thumbnail pull-left', 'zan-thumbnail animated flipInY','article-thumbnail animated flipInY']
def get_html_code(url):
    # print(url)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
    req = url_req.Request(url,headers=headers)
    response = url_req.urlopen(req).read().decode()
    soup = bsp4(response, 'html.parser')
    return soup
html = get_html_code(url)


data_list = []
# for i in class_name:
#     data = html.find_all('div', {'class': i})
#     data_list.extend(data)


data = html.find_all('div', {'class': 'article-thumbnail animated flipInY'})
print(data)



'''
首页采集目标
大图:
links

zan-thumbnail animated flipInY > a :href > img :src
article-thumbnail pull-left  > a :href > div > img : src
article-thumbnail animated flipInY > a :href > div > img : src

'''
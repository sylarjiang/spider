from urllib import request as url_req
import re
from bs4 import BeautifulSoup as bsp4



headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
# url="http://www.8btc.com/"
url="http://www.huoxing24.com/"

req = url_req.Request(url, headers=headers)
response = url_req.urlopen(req).read().decode()
# print(response)

soup = bsp4(response,'html.parser')

### 因为测试网站的标签层级太多,导致BSP默认是用列表读取,而attrs,又只能在底层节点使用.因为底层没有下一级了是字符方式.

# 结构化输出,通过.(点属性)找到的是从同类标签开始匹配,直到找到结束标签,并将第一个结束标签前的所有标签匹配完毕
# print(soup.body)

# print(soup.body.div)

# 查找指定标签,查找所有名为index-news-list的块.find_all以列表方式输出,[0]是为了取一组数据调试

data = soup.find_all('div',{'class': 'index-news-list'})[0]
# print(data)

# data中的存储方式是这样的
# for k,v in enumerate(data):
#     print(k,'key: ---->')
#     print(v)


# 获取子节点,和上面的方法一样,这是bsp4内置的方法.

# clild = [ i for i in soup.children ]
# print(clild)

# 获取子孙节点,看起来一样,不同的是这个是吧每个子孙节点都分叉开来.子节点内容会包括孙节点,所以会出现重复内容(集合去重?),在不知道孙节点命名方式的时候可以使用
# for i in data.descendants:
#     print(i)

# 获取父节点
# for i in data.descendants:
#     print(i.parent)


# 获取父辈节点

# print(data)
# for i in data.descendants:
#     if i is None:
#         print(i)
#     else:
#         print(i.parent.name)




# css选择器

# address = data.find_all('a')[0]['href']
#
# print(address)


for i in soup.find_all('div',{'class': 'index-news-list'}):
    link = i.find_all('a')[0]['href']
    print(link)


#
#
# print(soup.a.attr)




















# print(soup.find_all('div',{'class': 'index-news-list'}))





# with urlopen(url) as html:
#     data = html.read()
#     print('Status:', html.status, html.reason)
#     for k, v in html.getheaders():
#         print('%s: %s' % (k, v))
#     print('Data:', data.decode('utf-8'))


# html = urlopen(url).read().decode('utf8')
# # print(html)
# # data = re.findall(r"<a(.+?)</a>",html)
# data = re.findall(r'href="(.*?)"',html)
# for i in data:
#     print(i)


# html = request.Request(url).read().decode('utf8')
# soup = bsp4(html, 'html.parser')
#
# # res = soup.find_all('a')
# # data = res[500]['href']
# # print(data)
#
#
# res = soup.find_all('div', {'class': 'index-news-list'})
# data = res[0]
# data_soup = data.find_all('div', {'class': 'list-right'})


# news_address = data_soup.a['href']

# print(news_address)



# news_info['news_address']=data





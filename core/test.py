from urllib.request import urlopen
html = urlopen('http://www.chaindd.com/3101286.html')    # 用head方法去请求资源头部
print (html.getcode())  # 状态码


from core.db_conn import db_connected as db_func


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

def get_old_news_links(news_web_name=''):
    col = db_func(col='news_content')
    old_list = []
    for i in col.find({}, {'news_link': 1}):
        if i['news_link'].find(news_web_name):
            old_list.append(i['news_link'])
    return old_list

def links_changed(news_links,news_web_name=''):
    old_links = get_old_news_links(news_web_name)
    news_links_all = set(news_links) | (set(old_links))
    diff_links = set(news_links) - (set(old_links))
    return diff_links,news_links_all



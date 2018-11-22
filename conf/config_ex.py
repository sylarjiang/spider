import os,sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
DB_CONFIG = {
    'host' : '192.168.1.200',
    'port' : 27017,
    'auth_db' : 'news_spider',
    'username' : 'root',
    'password' : 'gtl1023'
}


linux_drive = '/usr/bin/chromedriver'
win_drive = 'D:/git/spider/core/chromedriver.exe'

browserdrive = win_drive

#线上
#category_id = '5b891c4b5dc0ab7f53602a11'
#测试环境
category_id = '5b7e4ce1c3e9de24a90b9823'

sys.path.insert(0, BASE_DIR)



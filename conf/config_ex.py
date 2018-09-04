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

category_id = '5b891c4b5dc0ab7f53602a11'



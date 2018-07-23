from conf import config
import pymongo
import sys
import traceback


mongo_conf = config.MONGODB_CONFIG
# print(mongo_conf)
class MongoConn(object):
    def __init__(self):
        try:
            self.conn = pymongo.MongoClient(mongo_conf['host'], mongo_conf['port'])
            self.db = self.conn[mongo_conf['db_name']]
            self.username = mongo_conf['username']
            self.password = mongo_conf['password']
            if self.username and self.password:
                self.connected = self.db.authenticate(self.username, self.password)
            else:
                self.connected = True

        except Exception:
            print(traceback.format_exc())
            print('Connect Statics Database Fail.')
            sys.exit(1)



db = MongoConn()
# spider_col = db()

from core import hx_news
news = hx_news.news


# json和写入文件
import json
newsobj = json.dumps(news)

with open('test.txt','w+',) as f:
    f.write(str(news))
    f.close()






































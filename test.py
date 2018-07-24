from pymongo import MongoClient




post = {

    'link' : 'ssss',
}


# uri = 'mongodb://root:gtl1023@192.168.1.222/?authSource=admin'
import urllib.parse
username = urllib.parse.quote_plus('root')
password = urllib.parse.quote_plus('gtl1023')
print(username,password)
# client = MongoClient("mongodb://%s:%s@192.168.1.200/?authSource=admin&authMechanism=SCRAM-SHA-1"%(username,password))
client = MongoClient("mongodb://root:gtl1023@192.168.1.200/?authSource=admin&authMechanism=SCRAM-SHA-1")
# client = pymongo.MongoClient(uri)

db = client['news_spider']
res = db.users.find()

mycol = db['test']
post={'name':'sylar'}
mycol.insert_one(post)

col = db.collection_names()
col_data = mycol.find()
print(col_data)

for i in col_data:
    print(i)








from pymongo import MongoClient

# from conf import config
# mongo_conf = config.MONGODB_CONFIG
def db_connected(db='news_spider', col='test',):
    uri = "mongodb://root:gtl1023@192.168.1.200/?authSource=admin&authMechanism=SCRAM-SHA-1"
    client = MongoClient(uri)
    use_db = client[db]
    if col is not 'test':
        use_col = use_db[col]
        return use_col
    return use_db


# # use db
# test1 = db_connected()
# col = test1['other']
# post = {'myname':'sylar'}
# col.insert_one(post)
# x=test1.collection_names()
# for i in x:
#     print(i)

# use col
# col = db_connected(col='one')
# post = {'myname':'sylar'}
# col.insert_one(post)
# x=col.find()
# for i in x:
#     print(i)

# col = db_connected(col='hx_news')
# x =col.find()
# for i in x:print(i)

























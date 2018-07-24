from core.db_conn import db_connected

from pymongo import MongoClient

# test_list = [{'_id':100, 'name':'tom', 'job': 'ops'},{'_id':99, 'name':'jerry', 'job': 'dev'}]
#
# col = db_connected(col='test')
# res = col.insert_many(test_list)
# print(res.inserted_ids)

# db = db_connected()

db = db_connected()
for i in db.collection_names():print(i)

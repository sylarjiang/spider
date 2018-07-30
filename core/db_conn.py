from pymongo import MongoClient

# from conf import config
# mongo_conf = config.MONGODB_CONFIG

def db_connected(db='news_spider', col=None,):
    '''
    连接mongodb函数，后期优化目标，面向对象和配置文件动态载入
    :param db: use db like this: db = db_connected()
    :param col: use col like this: col = db_connected(col=use_col)
    :return: 默认返回db,指定col返回集合
    '''

    #uri = "mongodb://root:saS8dhdsjkJDAJ88d3vuHD@35.190.172.26/admin?authSource=admin&authMechanism=SCRAM-SHA-1"
    # uri = 'mongodb://root:saS8dhdsjkJDAJ88d3vuHD@35.190.172.26/?authSource=hx_news&authMechanism=SCRAM-SHA-1'
    uri = "mongodb://root:gtl1023@192.168.1.200/"
    # uri = "mongodb://news_spider:gtl1023@192.168.1.200/?authSource=admin"
    client = MongoClient(uri)
    use_db = client[db]
    if col is None:
        return use_db
    use_col = use_db[col]

    return use_col


# uri = 'mongodb://root:saS8dhdsjkJDAJ88d3vuHD@35.190.172.26/?authSource=hx_news&authMechanism=SCRAM-SHA-1'
# uri = "mongodb://root:gtl1023@192.168.1.200/"
# clent = MongoClient(uri)
# db = clent['news_spider']
# col = db['hx_news']
# # col = db_connected(col='news_spider')
# # col.find()
# for i in col.find():
#     print(i)
































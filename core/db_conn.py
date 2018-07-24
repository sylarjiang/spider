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
    uri = "mongodb://root:gtl1023@192.168.1.200/?authSource=admin&authMechanism=SCRAM-SHA-1"
    client = MongoClient(uri)
    use_db = client[db]
    if col is None:
        return use_db
    use_col = use_db[col]
    return use_col
































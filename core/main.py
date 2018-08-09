from core import news_jinse,news_chaindd,news_8btc
from conf import config
import time

browserdrive = config.browserdrive

def main():
    news_jinse.main()
    time.sleep(3)
    news_chaindd.main()
    time.sleep(3)
    news_8btc.main()


if __name__ == '__main__':
    main()
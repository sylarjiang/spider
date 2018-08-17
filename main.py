from core import news_chaindd, news_8btc, news_jinse
from conf import config
import time

def main():

    for i in [news_chaindd, news_8btc, news_jinse]:
        try:
            i.main()
        except Exception as e:
            print(e)
        time.sleep(3)



if __name__ == '__main__':
    main()
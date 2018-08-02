from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup as bsp4
url = 'http://www.8btc.com/blockchain'


# html = get_html_code(url)
# print(html)

# chrome_option = Options()
# chrome_option.add_argument('--headless')
# chrome_option.add_argument('--disable-gpu')
browserdrive = 'D:/git/spider/core/chromedriver.exe'
driver = webdriver.Chrome(executable_path=browserdrive)
driver.get(url)
# a = driver.find_element_by_xpath("//i[contains(text(),' 加载更多')]")
while driver.find_element_by_id('load_more_list'):
    driver.find_element_by_id('load_more_list').click()
    time.sleep(3)
a = driver.page_source

print(a)



# driver.find_element_by_link_text('加载更多').click()




from time import sleep
import chromedriver_binary
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import re
import os

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--incognito')
options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(options = options)

driver.implicitly_wait(10)


# HTML取ってくる

driver.get('https://www.mizuhobank.co.jp/takarakuji/check/numbers/backnumber/index.html')
sleep(3)


latest_links = driver.find_elements_by_css_selector('tr.js-backnumber-temp-a > td:first-of-type > p > a')

backnumber_links = driver.find_elements_by_css_selector('tr.js-backnumber-temp-b > td > a')
urls = [e.get_attribute('href') for e in latest_links+backnumber_links]

dir_name = (os.path.dirname(os.path.abspath(__file__)))

for i,url in enumerate(urls):
    print('='*30, i, '='*30)
    print(url)

    driver.get(url)
    sleep(5)

    html = driver.page_source

    title = re.sub(r'[\\/:*?"<>|]+', '', driver.title)

    p = os.path.join(dir_name, 'html', rf'{title}')

    with open(p, 'w', encoding='UTF-8') as f:
        f.write(html)

sleep(3)
driver.quit        
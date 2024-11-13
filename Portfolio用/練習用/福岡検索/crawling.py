from time import sleep
from selenium import webdriver
import chromedriver_binary
import os


options = webdriver.ChromeOptions()
options.add_argument('--incognito')
options.add_argument('--headless')
options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(options= options)
driver.implicitly_wait(10)

driver.get('https://atsumaru.jp/area/7/list?sagid=all')

# 一番下までスクロール
height = driver.execute_script('return document.body.scrollHeight')
new_height = 0

while True:
    print(height)
    driver.execute_script(f'window.scrollTo(0, {height})')
    sleep(5)

    new_height = driver.execute_script('return document.body.scrollHeight')

    if height == new_height:
        break

    height = new_height

with open('company_list.html', 'w', encoding='UTF-8') as f:
    f.write(driver.page_source)

driver.quit()
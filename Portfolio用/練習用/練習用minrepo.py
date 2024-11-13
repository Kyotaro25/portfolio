import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
import calendar
import datetime

headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
}

df = pd.DataFrame()

# 何年の何月のデータを調べるかを記載

year = 2024 # 年を入力
month = 10 # 月を入力

sum = str(year) + '-' +str(month) + '-'
# 基本URL
url = f'https://min-repo.com/ranking/?chihou=%E8%BF%91%E7%95%BF&date={sum}'

max_page = calendar.monthrange(year,month)


d_list = []

for i in range(max_page[1]):
    access_url = url + f'{i+1}'
    
    r = requests.get(access_url, headers=headers, timeout=3)
    r.raise_for_status

    soup = BeautifulSoup(r.content, 'lxml')

    page_urls = soup.select('div.ichiran_title > a')
    

    for j,page_url in enumerate(page_urls):
        page_url = page_url.get('href')

        sleep(3)

        page_r = requests.get(page_url, headers=headers, timeout=3)
        page_r.raise_for_status

        page_soup = BeautifulSoup(page_r.content, 'lxml')

        area = page_soup.select_one('span.todofuken > a').text
        hall_name = page_soup.select_one('span.hall_name > a').text
        sousamai = page_soup.select_one('tr:-soup-contains("総差枚") > td').text
        # sousamai = page_soup.select_one('table.sou > tr:first-of-type > td').text
        avesamai = page_soup.select_one('tr:-soup-contains("平均差枚") > td').text
        averoll = page_soup.select_one('tr:-soup-contains("平均G数") > td').text
        day = datetime.date(year,month,i+1)
        

        
        print('='*50)
        d_list.append({
            '日にち':day.strftime('%Y/%m/%d'),
            '地域':area,
            'ホール名':hall_name,
            '総差枚':sousamai,
            '平均差枚':avesamai,
            '平均回転数':averoll
        })
        print(d_list[-1])

        if j > 20:
            break

df = pd.DataFrame(d_list)
df.to_csv('minrepo_kinki_2024-10.csv', index=None)        

from time import sleep
from bs4 import BeautifulSoup
import requests
import pandas as pd

#HTMLを読み込む
with open('company_list.html', 'r', encoding='UTF-8') as f:
    html = f.read()

# HTMLを読み込む
soup = BeautifulSoup(html, 'lxml')

# 会社名、住所、電話番号を取得する

a_tags = soup.select('span.bl_card2_ttl_text > a')

d_list = []
for i,a_tag in enumerate(a_tags):
    url = 'https://atsumaru.jp/' + a_tag.get('href')

    r = requests.get(url)
    r.raise_for_status

    sleep(3)

    page_soup = BeautifulSoup(r.content, 'lxml')

    company_name = page_soup.select_one('span.bl_card2_ttl_text').text
    address = page_soup.select_one('td:-soup-contains("地図はこちら") > p:first-of-type').text
    tel = page_soup.select_one('div.telNo > p > strong > a').text

    d_list.append({
        'company_name':company_name,
        'address':address,
        'tel':tel
    })
    print('='*30, i, '='*30)
    print(d_list[-1])

    if i > 10:
        break

df = pd.DataFrame(d_list)
df.to_csv('fukuoka_company_list.csv', index=None)
from time import sleep
from bs4 import BeautifulSoup
import requests
import os
from glob import glob
import pandas as pd
import re

def parse(soup, f_name):
    if '当せん番号' in f_name:
        trs = soup.select('section.section > table:first-of-type > tbody > tr:not(:first-child)')
        for tr in trs:
            time = tr.select_one('th > p').text
            day = tr.select_one('td:first-of-type > p').text
            number = tr.select_one('td:nth-of-type(2) > p').text

            yield{
                'time': time,
                'day': day,
                'number': number
            }

    elif 'バックナンバー' in f_name:
        trs = soup.select('section.section > table> tbody > tr:not(:first-child)')
        for tr in trs:
            time = tr.select_one('th').text
            day = tr.select_one('td:first-of-type').text
            number = tr.select_one('td:nth-of-type(2)').text

            yield{
                'time': time,
                'day': day,
                'number': number
            }

    else:
        tables = soup.select('div.section__table-wrap > table:first-of-type > tbody')
        for tabel in tables:
            time = tabel.select_one('tr:first-of-type > th:last-of-type').text
            day = tabel.select_one('tr:nth-of-type(2) > td').text
            number = tabel.select_one('tr:nth-of-type(3) > td > b').text

            yield {
                'time': time,
                'day': day,
                'number': number
            }

    



# htmlを読み込むPathの設定
dir_name = os.path.dirname(os.path.abspath(__file__))
html_path = os.path.join(dir_name, 'html', '*')

# for loopでHTMLの読み込み
d_list = []
for path in glob(html_path):
    with open(path, 'r', encoding="UTF-8") as f:
        html = f.read()

## BeautifulSoupでHTMLを解析
    f_name = os.path.basename(path)

    soup = BeautifulSoup(html, 'lxml')

    parsed_dicts = parse(soup, f_name)
    d_list += list(parsed_dicts)

    print(len(d_list))


## 必要な部分だけ取得して変数d_listに格納する
df = pd.DataFrame(d_list)
df['no'] = df.time.map(lambda s: re.sub('第|回', '', s)).astype(int)
df = df.sort_values('no').set_index('no')
print(df)

# dataframeの作成
df.to_csv('numbers.csv', index=None)


# to_csvを使う
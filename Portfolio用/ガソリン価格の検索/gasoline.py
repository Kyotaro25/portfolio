from selenium import webdriver
import chromedriver_binary
import tkinter
import time
from bs4 import BeautifulSoup
import requests
import pandas as pd
from time import sleep
import psycopg2
from sqlalchemy import create_engine

#optionの設定
options = webdriver.ChromeOptions()
options.add_argument('--incognito')
options.add_experimental_option('excludeSwitches', ['enable-logging']) 

driver = webdriver.Chrome(options=options)


#postgreSQLへの接続
connection_config = {
    'user': 'postgres',
    'password': 'postgres',
    'host':'localhost',
    'port': '5432',
    'database': 'gasoline'
}
engine = create_engine('postgresql://{user}:{password}@{host}:{port}/{database}'.format(**connection_config))

#URLを取ってくるイベントー処理まで
def reload_gasoline_search(event):
    #URLを取得
    base_url = 'https://gogo.gs/ranking/{}'

    for i in range(len(area_list)):
        if area_combobox.current() == i:
            area_url = (base_url.format(i))
            break
            
    driver.get(area_url)
    time.sleep(5)
    print(radio_value.get())

    #種類を検索
    for i in range(len(gas_list)):  
        if radio_value.get() == i:
            gasoline_change = driver.find_element_by_css_selector(f'ul.ranking-tab > li:nth-of-type({i+1}) > a')
            break

    gasoline_change.click()
    time.sleep(2)


    ##価格区分
    #会員のみの場合
    if boolean_money.get() == False and boolean_member.get() == True:
        #
        check_mo = driver.find_element_by_css_selector('#members_0')
        driver.execute_script("arguments[0].click();",check_mo)
        check_me = driver.find_element_by_css_selector('#members_1')
        driver.execute_script("arguments[0].click();",check_me)
    #現金、会員両方の場合
    if boolean_money.get() == True and boolean_member.get() == True:
        rcheck_me = driver.find_element_by_css_selector('#members_1')
        driver.execute_script("arguments[0].click();",rcheck_me)
    #両方チェック入っていない場合
    if boolean_money.get() == False and boolean_member.get() == False:
        rcheck_mo = driver.find_element_by_css_selector('#members_0')
        driver.execute_script("arguments[0].click();",rcheck_mo)

    ##タイプ
    type_search = ['#h24','#self','#staff']
    for i in range(len(boolean_type)):
        if boolean_type[i].get() == True:
            rtype = driver.find_element_by_css_selector(type_search[i])
            driver.execute_script("arguments[0].click();",rtype)

    ##系列
    company_search = ['#maker_3','#maker_8','#maker_6','#maker_4','#maker_11','#maker_14','#maker_15','#maker_12','#maker_99']
    for i in range(len(boolean_company)):
        if boolean_company[i].get() == True:
            rcompany = driver.find_element_by_css_selector(company_search[i])
            driver.execute_script("arguments[0].click();",rcompany)

    
    searchbutton = driver.find_element_by_css_selector('input[value="絞り込み"]')
    searchbutton.click()

    #HTMLを読み込む
    html = driver.current_url
    r = requests.get(html, timeout=3)
    r.raise_for_status

    soup = BeautifulSoup(r.content, 'lxml')

        #最大ページ数を取得
    total = soup.select_one('div.number').text
    target = ' '
    idx = total.find(target)
    r_total = int(total[idx+3:])
    print(r_total)

    #初期の最大ページを設定
    max_page = 1

    #トータルが20以上の場合の最大ページを取得
    if(r_total > 20):
        a_tag = soup.select_one('ul.pagination > li:last-of-type > a')
        r_url =(a_tag.get('href'))
        target2 = 'page='
        idx2 = r_url.find(target2)
        max_page = int(r_url[idx2+len(target2):])

    d_list = []

    for i in range(max_page):
        base_url = html + '&page={}'
        page_url = base_url.format(i+1)
        print(page_url)
        page_r = requests.get(page_url)
        sleep(3)
        page_r.raise_for_status 
    
        page_soup = BeautifulSoup(page_r.content, 'lxml')

        gasoline_type = page_soup.select_one('ul.ranking-tab > li.active > a').text

        names = page_soup.select('div.card > table > tr:nth-child(odd)') #不要なtrタグを除去


        for name in names:
            rank = int(name.select_one('div.rank').text)
            gas = gasoline_type
            mtype = name.select_one('td.price-td > div:last-of-type').text
            price = int(name.select_one('div.price').text)
            shop = name.select_one('a.shop-name').text
            address = name.select_one('p.address').text

            
            d_list.append({
                'rank' : rank,
                'type' : gas,
                'mtype' : mtype,
                'price' : price,
                'shop' : shop,
                'address' : address
            })
            print('='*30, rank, '='*30)
            print(d_list[-1])
        
    df = pd.DataFrame(d_list)    
    ##CSV形式で保存
    # df.to_csv('gasolin.csv', index=None)

    ##データベースに保存
    from sqlalchemy.dialects.postgresql import INTEGER
    from sqlalchemy.dialects.postgresql import TEXT
    df.to_sql('gastable',schema='public', con=engine,if_exists='replace', index=False,dtype={'rank':INTEGER,'gas':TEXT,'mtype':TEXT,'price':INTEGER,'shop':TEXT,'address':TEXT})
    
    print("----Finish!----")



## UI作成



app = tkinter.Tk()
app.title(u'ガソリン価格の検索')
app.geometry("790x410")
label_font = 'Helvetica'
top_frame = tkinter.Frame(app)
top_frame.grid(row=0,column=0)
condition_frame = tkinter.Frame(app)
condition_frame.grid(row=1,column=0)


# エリアの設定
import tkinter.ttk as ttk
area_frame = tkinter.LabelFrame(top_frame,text='エリアを設定',font=label_font,bg='salmon')
area_frame.grid(row=1,column=1,padx=40,pady=0,ipadx=0,ipady=0,sticky=tkinter.N)
area_list = ['全国','北海道','青森','岩手','宮城','秋田','山形','福島','茨城','栃木','群馬','埼玉','千葉','東京','神奈川','新潟','富山',
          '石川','福井','山梨','長野','岐阜','静岡','愛知','三重','滋賀','京都','大阪','兵庫','奈良','和歌山','鳥取','島根',
          '岡山','広島','山口','徳島','香川','愛媛','高知','福岡','佐賀','長崎','熊本','大分','宮崎','鹿児島','沖縄']
area_static = tkinter.Label(area_frame, text=u"都道府県を選択してください",bg='orange',font=label_font)
area_static.grid(row=2,column=1,padx=18,pady=0,ipadx=0,ipady=2,sticky=tkinter.W)
area_combobox = ttk.Combobox(area_frame, width=20,height=10, values=area_list, font=("Helvetica",12,"bold"))
area_combobox.grid(row=3, column=1, padx=20,pady=2,ipadx=87,ipady=0)


# ガソリンの種類
radio_frame = tkinter.Label(condition_frame,text='ガソリンの種類',bg='gainsboro',relief='solid',font=label_font)
radio_frame.grid(row=0,column=0,padx=10,pady=0,ipadx=10,ipady=7,sticky=tkinter.N)
radio_value = tkinter.IntVar()
gas_list = ['レギュラー','ハイオク','軽油','灯油']
gas_bg = ['red','gold','green4','cornflower blue']
radio_gas = []

inner_radioframe = tkinter.LabelFrame(condition_frame,background='white')
inner_radioframe.grid(row=1,column=0,padx=15,pady=0,ipadx=0,ipady=0,sticky=tkinter.N)

for i in range(len(gas_list)):
    radio_gas.append(tkinter.Radiobutton(inner_radioframe,text=gas_list[i],variable=radio_value,value=i,background=gas_bg[i],justify='left',font=label_font))
    radio_gas[i].grid(row=i, column=0, padx=0,pady=2,ipadx=0,ipady=0,sticky=tkinter.W)



##価格区分(組み合わせを使用したいため、for文は使用しない)
section_label = tkinter.Label(condition_frame,text='価格区分',bg='SteelBlue1',relief='ridge',font=label_font)
section_label.grid(row=0,column=1,padx=0,pady=0,ipadx=10,ipady=7,sticky=tkinter.N)
section_list = ['現金','会員']

inner_sectionframe = tkinter.LabelFrame(condition_frame)
inner_sectionframe.grid(row=1,column=1,padx=20,pady=0,ipadx=0,ipady=0,sticky=tkinter.N)

#現金
boolean_money = tkinter.BooleanVar()
boolean_money.set(True) #初期状態ではオンに
check_money = tkinter.Checkbutton(inner_sectionframe, variable = boolean_money, width =1)
check_money.grid(row = 0, column=0, padx=0,pady=0,ipadx=0,ipady=0)
label_money=tkinter.Label(inner_sectionframe,width=0,text=section_list[0],background='white',anchor='w',font=label_font)
label_money.grid(row=0, column=1, padx=0,pady=0,ipadx=0,ipady=0)
#会員
boolean_member = tkinter.BooleanVar()
boolean_member.set(False) #初期状態ではオフに
check_member = tkinter.Checkbutton(inner_sectionframe, variable = boolean_member, width =1)
check_member.grid(row=1, column=0, padx=0,pady=0,ipadx=0,ipady=0)
label_member=tkinter.Label(inner_sectionframe,width=0,text=section_list[1],background='white',anchor='w',font=label_font)
label_member.grid(row=1 , column=1, padx=0,pady=0,ipadx=0,ipady=0)


#タイプ(for文で作成)
type_label = tkinter.Label(condition_frame,text='タイプ',bg='SteelBlue1',relief='ridge',font=label_font)
type_label.grid(row=0,column=2,padx=0,pady=0,ipadx=10,ipady=7,sticky=tkinter.N)
type_list = ['24時間営業','セルフ','スタッフ給油']
boolean_type = []
check_type = []
label_type = []

inner_typeframe = tkinter.LabelFrame(condition_frame)
inner_typeframe.grid(row=1,column=2,padx=20,pady=0,ipadx=0,ipady=0,sticky=tkinter.N)

for i in range(len(type_list)):
    boolean_type.append(tkinter.BooleanVar())
    boolean_type[i].set(False) #初期状態ではオフ
    check_type.append(tkinter.Checkbutton(inner_typeframe, variable = boolean_type[i], width =1))
    check_type[i].grid(row = i, column=0, padx=0,pady=0,ipadx=0,ipady=0)
    label_type.append(tkinter.Label(inner_typeframe,width=0,text=type_list[i],background='white',anchor='w',font=label_font))
    label_type[i].grid(row= i, column=1, padx=0,pady=0,ipadx=0,ipady=0)


#系列(for文で作成)
company_label = tkinter.Label(condition_frame,text='系列',bg='SteelBlue1',relief='ridge',font=label_font)
company_label.grid(row=0,column=3,padx=0,pady=0,ipadx=10,ipady=7,sticky=tkinter.N)
company_list = ['ENEOS','apollostation','コスモ石油','KYGNUS','SOLATO','carenex','三菱商事エネルギー','JA-SS','独自・その他']
boolean_company = []
check_company = []
label_company = []

inner_companyframe = tkinter.LabelFrame(condition_frame)
inner_companyframe.grid(row=1,column=3,padx=20,pady=0,ipadx=0,ipady=0,sticky=tkinter.N)

for i in range(len(company_list)):
    boolean_company.append(tkinter.BooleanVar())
    boolean_company[i].set(False) #初期状態ではオフ
    check_company.append(tkinter.Checkbutton(inner_companyframe, variable = boolean_company[i], width =1))
    check_company[i].grid(row = i, column=0, padx=0,pady=0,ipadx=0,ipady=0)
    label_company.append(tkinter.Label(inner_companyframe,width=0,text=company_list[i],background='white',anchor='w',font=label_font))
    label_company[i].grid(row= i, column=1, padx=0,pady=0,ipadx=0,ipady=0)


##入力完了確認ボタン##
button_frame = tkinter.Frame(app)
button_frame.grid(row=2,column=0)

enter_button = tkinter.Button(button_frame,text=u'OK',font=label_font)
enter_button.grid(row=4,column=1,padx=0,pady=0,ipadx=0,ipady=0)
enter_button.bind('<Button-1>',reload_gasoline_search)
time.sleep(3)


app.mainloop()
# !/Python

import requests
import sqlite3
import threading

########--Tools--########

def sscode(code):
    if str(code)[0]+str(code)[1] =='60':
        code = 'sh%s' % code
    else:
        code = 'sz%s' % code
    return code

def share_name(code):
    s = requests.session()
    s.keep_alive = False
    url = 'http://hq.sinajs.cn/list=%s' % sscode(code)
    r = None
    while r == None:
        r = s.get(url, timeout=2)
    name = r.text.split("\"")[1].split(",",1)[0]
    return name

#######--sqlite3--#######

def delete_form(dbname, formname):
    conn = sqlite3.connect('database/%s.db' % dbname)
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS %s;" % formname)
    conn.commit()
    conn.close()
    print("Form %s Deleted!" % formname)

def create_form(dbname, formname):
    conn = sqlite3.connect('database/%s.db' % dbname)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS %s
        (CODE INTEGER PRIMARY KEY UNIQUE,
        NAME   TEXT);''' % formname)
    conn.commit()
    conn.close()
    print("Form %s Created!" % formname)

def insert_data(dbname, formname, code):
    name = share_name(code)
    conn = sqlite3.connect('database/%s.db' % dbname)
    c = conn.cursor()
    c.execute("INSERT INTO %s (CODE, NAME) VALUES (?, ?)" % formname,(code, name))
    conn.commit()
    conn.close()

#########################

def get_stocks_list():
    global ashare_list
    ashare_list = []
    url = 'http://query.sse.com.cn/security/stock/getStockListData2.do?&stockType=1&pageHelp.beginPage=1&pageHelp.pageSize=2000'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0',
        'Referer': 'http://www.sse.com.cn/assortment/stock/list/share/'
    }
    stock_data = requests.get(url, headers = header).json()['pageHelp']['data']
    for i in range(len(stock_data)):
        print(i)
        code = stock_data[i]['SECURITY_CODE_A']
        listing_date = stock_data[i]['LISTING_DATE']
        if listing_date != '-':
            d = listing_date.split('-')
            n = int(d[0]+d[1]+d[2])
            if n < 20171201:
                ashare_list.append(code)
                print('%s Added!' % code)
    print('Found %d Stocks!' % len(ashare_list))

def check_stop(stock_code):
    print('Checking Stop %s...' % stock_code)
    s = requests.session()
    s.keep_alive = False
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'}
    url = 'http://hq.sinajs.cn/list=%s' % sscode(stock_code)
    r = None
    while r == None:
        r = s.get(url, headers=header, timeout=1)
    if r.text.split("\"")[1].split(",")[1] > 18:
        ashare_list.remove(stock_code)
    elif r.text.split("\"")[1].split(",")[8] == '0':
        if r.text.split("\"")[1].split(",")[10] == '0':
            if r.text.split("\"")[1].split(",")[12] == '0':
                ashare_list.remove(stock_code)
def get_list():
    get_stocks_list()
    a = len(ashare_list)
    for i in ashare_list:
        check_stop(i)
    b = len(ashare_list)
    print(a, b, a-b)

def insert():
    for i in ashare_list:
        insert_data('instance', 'sh', i)
    print('All Data Inserted!')

get_list()
delete_form('instance', 'sh')
create_form('instance', 'sh')
#for i in ashare_list:
#    insert_data('instance', 'sh', i)

t = threading.Thread(target=insert)
t.start()



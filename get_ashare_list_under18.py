# !/Python

import requests
import sqlite3
import threading
from datetime import date


############PROXY###########

proxies = {
    "https": "http://122.72.18.34:80"

}

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

#######---get-live-data---#######

def price_now(stock_code):
    s = requests.session()
    s.keep_alive = False
    url = 'http://api.finance.ifeng.com/aminhis/?code=%s&type=five' % sscode(stock_code)
    now = s.get(now_url, timeout=5).json()[-1]['record'][-1]
    # Price
    price = float(now[1])
    # Average
    average = float(now[4])
    return (price, average)

def ma_now(stock_code):
    today = date.today()
    span = '%s%s%s' % (today.year, today.month, today.day)
    url = 'http://pdfm.eastmoney.com/EM_UBG_PDTI_Fast/api/js?id=%s1&TYPE=k&rtntype=1&QueryStyle=2.2&QuerySpan=%s%%2C1&extend=ma' % (stock_code, span)
    s = requests.session()
    s.keep_alive = False
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'}
    ma = s.get(url, headers= header, proxies=proxies, timeout=3)
    ma_data = ma.text.split('[')[1].split(']')[0].split(',')
    ma5 = float(ma_data[0])
    ma10 = float(ma_data[1])
    ma20 = float(ma_data[2])
    return(ma5, ma10)

#######---plot---#######
import pylab as pl

def plot_ma(TITLE, MA5, MA10, DATE):
    pl.title(TITLE)
    a, = pl.plot(DATE, MA5, 'r-')
    b, = pl.plot(DATE, MA10, 'b-')
    pl.legend([a, b], ('MA5', 'MA10'), numpoints=1)
    pl.savefig('stock/%s.png' % TITLE)
    pl.close()
    print('Plot %s success' % TITLE)

def get_ma(stock_code):
    ua_mo = 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_1_1 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0 Mobile/15B150 Safari/604.1'
    header = {'User-Agent':ua_mo}
    ma_url = 'http://api.finance.ifeng.com/akdaily/?code=%s&type=last' % stock_code
    now_url = 'http://api.finance.ifeng.com/aminhis/?code=%s&type=five' % stock_code
    now = requests.get(now_url, headers = header).json()[-1]['record'][-1]
    ma = requests.get(ma_url, headers = header).json()['record']
    # MA5
    ma5_now = float(now[4])
    ma5_1 = float(ma[-1][8])
    ma5_2 = float(ma[-2][8])
    ma5_3 = float(ma[-3][8])
    ma5_4 = float(ma[-4][8])
    ma5_5 = float(ma[-5][8])
    ma5_6 = float(ma[-6][8])
    ma5_7 = float(ma[-7][8])
    ma5_8 = float(ma[-8][8])
    ma5_9 = float(ma[-9][8])
    ma5_10 = float(ma[-10][8])
    # MA10
    ma10_now = float(now[5])
    ma10_1 = float(ma[-1][9])
    ma10_2 = float(ma[-2][9])
    ma10_3 = float(ma[-3][9])
    ma10_4 = float(ma[-4][9])
    ma10_5 = float(ma[-5][9])
    ma10_6 = float(ma[-6][9])
    ma10_7 = float(ma[-7][9])
    ma10_8 = float(ma[-8][9])
    ma10_9 = float(ma[-9][9])
    ma10_10 = float(ma[-10][9])
    ma5_list = [ma5_1, ma5_2, ma5_3, ma5_4, ma5_5, ma5_6, ma5_7, ma5_8, ma5_9, ma5_10]
    ma10_list = [ma10_1, ma10_2, ma10_3, ma10_4, ma10_5, ma10_6, ma10_7, ma10_8, ma10_9, ma10_10]
    date_list = []
    for i in range(-1, -11, -1):
        date_list.append(ma[i][0].split('-',1)[1])
    return(stock_code, ma5_list, ma10_list, date_list)

def plot_images(CODE):
    a = get_ma(CODE)
    plot_ma(a[0], a[1], a[2], a[3])

def plot_list(listname):
    for i in globals()[str(listname)]:
        try:
            plot_images('sh'+i)
        except:
            pass


#########################
# 导入A股列表ashare_list并去除20171201以后上市的股票
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

# 去除ashare_list中停牌的股票
def check_suspended(stock_code):
    print('Checking Suspended %s...' % stock_code)
    s = requests.session()
    s.keep_alive = False
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'}
    url = 'http://hq.sinajs.cn/list=%s' % sscode(stock_code)
    r = None
    while r == None:
        r = s.get(url, headers=header, timeout=1)
    if float(r.text.split("\"")[1].split(",")[1]) > 18:
        ashare_list.remove(stock_code)
    elif r.text.split("\"")[1].split(",")[8] == '0':
        if r.text.split("\"")[1].split(",")[10] == '0':
            if r.text.split("\"")[1].split(",")[12] == '0':
                ashare_list.remove(stock_code)

# MA10连续n日大于MA5,导出至watchlist
def sort_watchlist(stock_code):
    print('Watching %s' %stock_code)
    ua_mo = 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_1_1 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0 Mobile/15B150 Safari/604.1'
    header = {'User-Agent':ua_mo}
    ma_url = 'http://api.finance.ifeng.com/akdaily/?code=%s&type=last' % sscode(stock_code)
    ma = requests.get(ma_url, headers = header).json()['record']
    # MA5
    ma5_1 = float(ma[-1][8])
    ma5_2 = float(ma[-2][8])
    ma5_3 = float(ma[-3][8])
    ma5_4 = float(ma[-4][8])
    ma5_5 = float(ma[-5][8])
    ma5_6 = float(ma[-6][8])
    ma5_7 = float(ma[-7][8])
    ma5_8 = float(ma[-8][8])
    ma5_9 = float(ma[-9][8])
    ma5_10 = float(ma[-10][8])
    # MA10
    ma10_1 = float(ma[-1][9])
    ma10_2 = float(ma[-2][9])
    ma10_3 = float(ma[-3][9])
    ma10_4 = float(ma[-4][9])
    ma10_5 = float(ma[-5][9])
    ma10_6 = float(ma[-6][9])
    ma10_7 = float(ma[-7][9])
    ma10_8 = float(ma[-8][9])
    ma10_9 = float(ma[-9][9])
    ma10_10 = float(ma[-10][9])
    # 
    if ma10_1 > ma5_1:
        if ma10_2 > ma5_2:
            if ma10_3 > ma5_3:
                if ma10_4 > ma5_4:
                    if ma10_5 > ma5_5:
                        if ma10_6 > ma5_6:
                            if ma10_7 > ma5_7:
                                if ma10_8 > ma5_8:
                                    if ma10_9 > ma5_9:
                                        if ma10_10 > ma5_10:
                                            if ma5_2 < ma5_1:
                                                watchlist.append(stock_code)
                                                globals()['hist'+str(stock_code)] = (ma5_1, ma10_1)
                                                print('-----已经添加 %s 至watchlist 并获取MA5/10历史数据-----' % stock_code)

def get_watchlist():
    global watchlist
    watchlist = []
    for i in ashare_list:
        sort_watchlist(i)
    print('wacthlist finished!')
    print(len(watchlist))

# 获取MA5/10历史数据至hist600000
def get_ma_hist(stock_code):
    print('Getting %s Data' % stock_code)
    s = requests.session()
    s.keep_alive = False
    url =  'http://api.finance.ifeng.com/akdaily/?code=%s&type=last' % sscode(stock_code)
    r = s.get(url, timeout=5)
    ma = r.json()['record']
    # MA5
    ma5_1 = float(ma[-1][8])
    ma5_2 = float(ma[-2][8])
   # MA10
    ma10_1 = float(ma[-1][9])
    if ma5_2 < ma5_1:
        globals()['hist'+str(stock_code)] = (ma5_1, ma10_1)
    else:
        ashare_list.remove(stock_code)

def get_hist_data():
    for i in watchlist:
        get_ma_hist(i)
    print('All HIST DATA GOT!')

def get_list():
    get_stocks_list()
    a = len(ashare_list)
    for i in ashare_list:
        check_suspended(i)
    b = len(ashare_list)
    print(a, b, a-b)

def insert():
    for i in ashare_list:
        insert_data('instance', 'sh_under18', i)
    print('All Data Inserted!')

def watching(stock_code):
    hist = globals()['hist'+str(stock_code)]
    ma = ma_now(stock_code)
    if ma[0] > ma[1]:
        if ma[0] > hist[0] and ma[1] > hist[1]:
            buy_list.append(stock_code)
            print('%s买入时机' % stock_code)

def watch(listname):
    global buy_list
    buy_list = []
    while 1:
        print('开始')
        for i in globals()[listname]:
            watching(i)


get_list()
delete_form('instance', 'sh_under18')
create_form('instance', 'sh_under18')
#for i in ashare_list:
#    insert_data('instance', 'sh', i)

t = threading.Thread(target=insert)
t.start()
get_watchlist()
#plot_list('watchlist')
#get_hist_data()
watch('watchlist')

            




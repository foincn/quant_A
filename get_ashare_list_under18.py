# !/Python

import requests
import sqlite3
import threading
from multiprocessing import Process
import time
from bs4 import BeautifulSoup
from datetime import date

############PROXY###########

proxies = {
    "https": "http://165.227.100.201:80",
    "https": "http://183.235.254.159:8080",
    "https": "http://183.235.254.159:8080"
}
proxies = None

########--Tools--########

def sscode(code):
    code = str(code)
    if code[0]+code[1] =='60':
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
        (CODE TEXT PRIMARY KEY UNIQUE,
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
    r = None
    while r == None:
        try:
            r = s.get(url, timeout=3)
        except:
            pass
    if r.text == '':
        print('无法获取 %s 价格。' % stock_code)
        price = ''
        average = ''
    else:
        now = r.json()[-1]['record'][-1]
        # Price
        price = float(now[1])
        # Average
        average = float(now[4])
    return (price, average)

def ma_now(stock_code, debug=0):
    today = date.today()
    span = '%s%s%s' % (today.year, today.month, today.day)
    url = 'http://pdfm.eastmoney.com/EM_UBG_PDTI_Fast/api/js?id=%s1&TYPE=k&rtntype=1&QueryStyle=2.2&QuerySpan=%s%%2C1&extend=ma' % (stock_code, span)
    s = requests.session()
    s.keep_alive = False
    r = None
    while r == None:
        try:
            r = s.get(url, proxies=proxies, timeout=3)
        except:
            pass
    if debug != 0:
        return r
    if r.text == '({stats:false})':
        ma5 = ''
        ma10 = ''
    else:
        ma_data = r.text.split('[')[1].split(']')[0].split(',')
        ma5 = float(ma_data[0])
        ma10 = float(ma_data[1])
        ma20 = float(ma_data[2])
    #print(ma5, ma10)
    return(ma5, ma10)

def ma_hist(stock_code, days=10, debug=0):
    #ua_mo = 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_1_1 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0 Mobile/15B150 Safari/604.1'
    #header = {'User-Agent':ua_mo}
    s = requests.session()
    s.keep_alive = False
    url = 'http://api.finance.ifeng.com/akdaily/?code=%s&type=last' % sscode(stock_code)
    r = None
    while r == None:
        try:
            r = s.get(url, proxies=proxies, timeout=5)
        except:
            pass
    if debug != 0:
        return r
    ma = r.json()['record']
    ma5 = []
    ma10 = []
    if ma == {}:
        pass
    else:
        if len(ma) < days:
            pass
        else:
            for l in range(days):
                ma5.append(float(ma[-l-1][8]))
                ma10.append(float(ma[-l-1][9]))
    return(ma5, ma10)


#######---plot---#######
import pylab as pl
from matplotlib.font_manager import FontProperties  

def plot_ma(stock_code, MA5, MA10, DATE, listname):
    font = FontProperties(fname="/usr/share/fonts/opentype/noto/NotoSansCJK-Medium.ttc", size=14)
    title = '%s %s' % (stock_code, share_name(stock_code))
    pl.title(title, fontproperties=font)
    a, = pl.plot(DATE, MA5, 'r-')
    b, = pl.plot(DATE, MA10, 'b-')
    pl.legend([a, b], ('MA5', 'MA10'), numpoints=1)
    pl.savefig('stock/%s/%s.png' % (listname, sscode(stock_code)))
    pl.close()
    print('Plot %s success' % title)

def get_ma(stock_code):
    ua_mo = 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_1_1 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0 Mobile/15B150 Safari/604.1'
    header = {'User-Agent':ua_mo}
    ma_url = 'http://api.finance.ifeng.com/akdaily/?code=%s&type=last' % sscode(stock_code)
    now_url = 'http://api.finance.ifeng.com/aminhis/?code=%s&type=five' % sscode(stock_code)
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

def plot_images(CODE, listname):
    a = get_ma(CODE)
    plot_ma(a[0], a[1], a[2], a[3], listname)

def plot_list(listname):
    for i in globals()[str(listname)]:
        try:
            plot_images(i, listname)
        except:
            pass


##############################################
# 导入股票
def get_list(listname='share_list'):
    globals()[listname] = []
    get_sha_list()
    get_sza_list()
    get_szzx_list()
    get_szcy_list()
    globals()[listname] = list(set(globals()[listname]))
    #check_suspended_list()
    print('成功导入 %s 支股票。' % len(globals()[listname]))

# 导入上海A股列表share_list并去除20171201以后上市的股票
def get_sha_list(listname='share_list'):
    if listname in globals().keys():
        if listname != 'share_list':
            globals()[listname] = []
    else:
        globals()[listname] = []
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
                globals()[listname].append(code)
                print('%s Added!' % code)
        else: 
            globals()[listname].append(code)
            print('%s Added!' % code)
    print('Found %d Stocks!' % len(globals()[listname]))

# 导入深圳A股列表share_list并去除20171201以后上市的股票
def get_sza_list(listname='share_list'):
    if listname in globals().keys():
        if listname != 'share_list':
            globals()[listname] = []
    else:
        globals()[listname] = []
    s = requests.session()
    s.keep_alive = False
    index_url = 'http://www.szse.cn/szseWeb/FrontController.szse?ACTIONID=7&AJAX=AJAX-FALSE&CATALOGID=1110&TABKEY=tab2&tab2PAGENO=1'
    index_html = s.get(index_url).content
    index_soup = BeautifulSoup(index_html, "html.parser")
    index = int(index_soup.select('td')[-3].text.split()[1][1:-1])
    print(index)
    for i in range(index):
        i = i + 1
        print('获取第%s页数据，一共%s页。' % (i, index))
        url = 'http://www.szse.cn/szseWeb/FrontController.szse?ACTIONID=7&AJAX=AJAX-FALSE&CATALOGID=1110&TABKEY=tab2&tab2PAGENO=%s' % i
        html = s.get(url).content
        soup = BeautifulSoup(html, "html.parser")
        source = soup.select('tr[bgcolor="#ffffff"]')
        source1 = soup.select('tr[bgcolor="#F8F8F8"]')
        source += source1
        for l in source:
            code = l.select('td')[2].text
            print(code)
            listing_date = l.select('td')[4].text
            print(listing_date)
            if listing_date != '-':
                d = listing_date.split('-')
                n = int(d[0]+d[1]+d[2])
                if n < 20171201:
                    globals()[listname].append(code)
                    print('%s Added!' % code)
            else: 
                globals()[listname].append(code)
                print('%s Added!' % code)

# 导入深圳中小板列表share_list
def get_szzx_list(listname='share_list'):
    if listname in globals().keys():
        if listname != 'share_list':
            globals()[listname] = []
    else:
        globals()[listname] = []
    s = requests.session()
    s.keep_alive = False
    index_url = 'http://www.szse.cn/szseWeb/FrontController.szse?ACTIONID=7&AJAX=AJAX-FALSE&CATALOGID=1110&TABKEY=tab5&tab5PAGENO=1'
    index_html = s.get(index_url).content
    index_soup = BeautifulSoup(index_html, "html.parser")
    index = int(index_soup.select('td')[-3].text.split()[1][1:-1])
    print(index)
    for i in range(index):
        i = i + 1
        print('获取第%s页数据，一共%s页。' % (i, index))
        url = 'http://www.szse.cn/szseWeb/FrontController.szse?ACTIONID=7&AJAX=AJAX-FALSE&CATALOGID=1110&TABKEY=tab5&tab5PAGENO=%s' % i
        html = s.get(url).content
        soup = BeautifulSoup(html, "html.parser")
        source = soup.select('tr[bgcolor="#ffffff"]')
        source1 = soup.select('tr[bgcolor="#F8F8F8"]')
        source += source1
        for l in source:
            code = l.a.u.text
            globals()[listname].append(code)
            print('%s Added!' % code)

# 导入深圳创业板列表share_list
def get_szcy_list(listname='share_list'):
    if listname in globals().keys():
        if listname != 'share_list':
            globals()[listname] = []
    else:
        globals()[listname] = []
    s = requests.session()
    s.keep_alive = False
    index_url = 'http://www.szse.cn/szseWeb/FrontController.szse?ACTIONID=7&AJAX=AJAX-FALSE&CATALOGID=1110&TABKEY=tab6&tab6PAGENO=1'
    index_html = s.get(index_url).content
    index_soup = BeautifulSoup(index_html, "html.parser")
    index = int(index_soup.select('td')[-3].text.split()[1][1:-1])
    print(index)
    for i in range(index):
        i = i + 1
        print('获取第%s页数据，一共%s页。' % (i, index))
        url = 'http://www.szse.cn/szseWeb/FrontController.szse?ACTIONID=7&AJAX=AJAX-FALSE&CATALOGID=1110&TABKEY=tab6&tab6PAGENO=%s' % i
        html = s.get(url).content
        soup = BeautifulSoup(html, "html.parser")
        source = soup.select('tr[bgcolor="#ffffff"]')
        source1 = soup.select('tr[bgcolor="#F8F8F8"]')
        source += source1
        for l in source:
            code = l.a.u.text
            globals()[listname].append(code)
            print('%s Added!' % code)

# 去除share_list中停牌的股票
def check_suspended(stock_code, listname='share_list'):
    print('Checking Suspended %s...' % stock_code)
    s = requests.session()
    s.keep_alive = False
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'}
    url = 'http://hq.sinajs.cn/list=%s' % sscode(stock_code)
    r = None
    while r == None:
        r = s.get(url, headers=header, timeout=1)
    if float(r.text.split("\"")[1].split(",")[1]) > 18:
        globals()[listname].remove(stock_code)
    elif r.text.split("\"")[1].split(",")[8] == '0':
        if r.text.split("\"")[1].split(",")[10] == '0':
            if r.text.split("\"")[1].split(",")[12] == '0':
                globals()[listname].remove(stock_code)

# 去除share_list中停牌的股票list
def check_suspended_list(listname='share_list'):
    li = list(globals()[listname])
    print(len(li))
    print('Checking list %s...' % listname)
    s = requests.session()
    s.keep_alive = False
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'}
    for i in globals()[listname]:
        rate = round(globals()[listname].index(i) / len(globals()[listname]) * 100, 2)
        print('Checking Suspended %s...     %s %%' % (i, rate))
        url = 'http://hq.sinajs.cn/list=%s' % sscode(i)
        r = None
        while r == None:
            r = s.get(url, headers=header, timeout=1)
        if float(r.text.split("\"")[1].split(",")[1]) > 18:
            li.remove(i)
        elif r.text.split("\"")[1].split(",")[8] == '0':
            if r.text.split("\"")[1].split(",")[10] == '0':
                if r.text.split("\"")[1].split(",")[12] == '0':
                    li.remove(i)
    a = len(globals()[listname])
    b = len(globals()[listname])
    globals()[listname] = li
    return(a, b, a-b)

####################################################
# 筛选股票
def sort_list(listname='share_list', price=18, day=10):
    a = len(globals()[listname])
    sort_price_list(listname, price)
    sort_ma_list(listname, day)
    b = len(globals()[listname])
    print('过滤掉%s支股票，还剩%s支股票' % (a-b, b))

# 筛选share_list中，价格低于18元, 并去除停牌。
def sort_price_list(listname='share_list', target_price=18):
    print('筛选%s中，价格低于%s元。' % (listname, target_price))
    li = list(globals()[listname])
    print(len(li))
    for i in globals()[listname]:
        print('检查 %s 价格是否低于%s元' % (i, target_price))
        rate = round(globals()[listname].index(i) / len(globals()[listname]) * 100, 2)
        price = price_now(i)[0]
        if price == '':
            li.remove(i)
            print('%s 无法获取价格。 %s %%' % (i, rate))
        elif price > target_price:
            li.remove(i)
            print('%s 不符合条件。 %s %%' % (i, rate))
    a = len(globals()[listname])
    b = len(li)
    globals()[listname] = li
    print('已经从 %s 移除 %s 支股票，列表中还剩 %s' % (listname, a-b, b))

# 筛选share_list中，MA10连续n日大于MA5。
def sort_ma_list(listname='share_list', days=10):
    print('筛选%s中MA10连续%s日大于MA5' % (listname, days))
    li = list(globals()[listname])
    print(len(li))
    for i in globals()[listname]:
        rate = round(globals()[listname].index(i) / len(globals()[listname]) * 100, 2)
        ma = ma_hist(i, days)
        if ma == ([], []):
            print('%s 获取数据失败！' % i)
            li.remove(i)
            continue
        for l in range(days):
            if ma[0][l] > ma[1][l]:
                li.remove(i)
                print('%s 不符合条件：MA10连续%s日大于MA5。' % (i, days))
                break
            if l == days-1:
                globals()['ma'+i] = (ma[0][0], ma[1][0])
                print('-----成功获取 %s MA5/10历史数据----- %s %%' % (i, rate))
    a = len(globals()[listname])
    b = len(li)
    globals()[listname] = li
    print('已经从 %s 移除 %s 支股票，列表中还剩 %s' %(listname, a-b, b) )



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
        share_list.remove(stock_code)

def get_hist_data():
    for i in watchlist:
        get_ma_hist(i)
    print('All HIST DATA GOT!')


def insert():
    for i in ashare_list:
        insert_data('instance', 'sh_under18', i)
    print('All Data Inserted!')

def ma_monitor(listname='share_list', count=9999):
    global buy_list
    buy_list = []
    c = 0
    while c < count:
        c += 1
        print('第%s次扫描, 一共%s支股票，已找到%s支股票符合。' % (c, len(globals()[listname]), len(buy_list)))
        # time.sleep(10)
        for i in globals()[listname]:
            ma_checker(i)

def ma_checker(stock_code):
    ma = ma_now(stock_code)
    if ma[0] > ma[1]:
        if ma[0] > globals()['ma'+stock_code][0] and  ma[1] > globals()['ma'+stock_code][1]:
            if stock_code not in buy_list:
                buy_list.append(stock_code)
                print('%s买入时机' % stock_code)

def ma_monitor_start(listname='share_list', count=9999):
    global b
    b = Process(target=ma_monitor, args=())
    b.start()

def ma_monitor_start(listname='share_list', count=9999):
    global a
    a = Process(target=ma_monitor, args=())

def get_watchlist():
    global watchlist
    watchlist = []
    for i in share_list:
        sort_watchlist(i)
    print('wacthlist finished!')
    print(len(watchlist))

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
    c = 0
    while 1:
        c += 1
        print('第%s次扫描, 已找到%s支股票。' % (c, len(buy_list)))
        # time.sleep(10)
        for i in globals()[listname]:
            watching(i)

############################
# 多线程筛选价格
def sort_price(share_code, target_price=18):
    print('检查 %s 价格是否低于%s元' % (share_code, target_price))
    price = price_now(share_code)[0]
    if price == '':
        li.remove(share_code)
        #print('%s 无法获取价格。' % share_code)
    elif price > target_price:
        li.remove(share_code)
        #print('%s 不符合条件。' % share_code)

def sort_price_t(listname='share_list', target_price=18):
    print('筛选%s中，价格低于%s元。' % (listname, target_price))
    global li
    li = list(globals()[listname])
    threads = []
    for i in globals()[listname]:
        a = threading.Thread(target=sort_price, args=(i, target_price))
        threads.append(a)
        a.start()
    for t in threads:
        t.join()
    a = len(globals()[listname])
    b = len(li)
    globals()[listname] = li
    print('已经从 %s 移除 %s 支股票，列表中还剩 %s' % (listname, a-b, b))

# 多线程筛选MA
def sort_ma(share_code, days=10):
    ma = ma_hist(share_code, days)
    if ma == ([], []):
        print('%s 获取数据失败！' % share_code)
        li.remove(share_code)
    else:
        for l in range(days):
            if ma[0][l] > ma[1][l]:
                li.remove(share_code)
                print('%s 不符合条件：MA10连续%s日大于MA5。' % (share_code, days))
                break
            if l == days-1:
                globals()['ma'+share_code] = (ma[0][0], ma[1][0])
                print('-----成功获取 %s MA5/10历史数据-----' % share_code)

def sort_ma_t(listname='share_list', days=10):
    print('筛选%s中MA10连续%s日大于MA5' % (listname, days))
    global li
    li = list(globals()[listname])
    threads = []
    for i in globals()[listname]:
        a = threading.Thread(target=sort_ma, args=(i, days))
        threads.append(a)
        a.start()
    for t in threads:
        t.join()
    a = len(globals()[listname])
    b = len(li)
    globals()[listname] = li
    print('已经从 %s 移除 %s 支股票，列表中还剩 %s' % (listname, a-b, b))


#############################

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
##############################
print('''
get_list()
    get_sha_list()
    get_sza_list()
    get_szzx_list()
    get_szcy_list()
sort_list()
    sort_price_list()
    sort_ma_list()
ma_monitor()
''')
get_szzx_list("szzx")
sort_ma_list("szzx", 20)

import code
code.interact(banner = "", local = locals())



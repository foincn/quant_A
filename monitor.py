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


#######---get-data---#######

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


#################--load-pages--####################

def get_sza_page(page_num, afterdate=20171201):
    # print('获取第%s页数据。' % page_num)
    url = 'http://www.szse.cn/szseWeb/FrontController.szse?ACTIONID=7&AJAX=AJAX-FALSE&CATALOGID=1110&TABKEY=tab2&tab2PAGENO=%s' % page_num
    s = requests.session()
    s.keep_alive = False
    r = None
    while r == None:
        try:
            r = s.get(url, timeout=3)
        except:
            pass
        else:
            pass
            #print('获取第%s页数据。' % page_num)
    html = r.content
    soup = BeautifulSoup(html, "html.parser")
    source = soup.select('tr[bgcolor="#ffffff"]')
    source1 = soup.select('tr[bgcolor="#F8F8F8"]')
    source += source1
    for l in source:
        code = l.select('td')[2].text
        listing_date = l.select('td')[4].text
        if listing_date != '-':
            d = listing_date.split('-')
            n = int(d[0]+d[1]+d[2])
            if n < afterdate:
                li.append(code)
        else: 
            li.append(code)

def get_szzx_page(page_num):
    # print('获取第%s页数据。' % page_num)
    url = 'http://www.szse.cn/szseWeb/FrontController.szse?ACTIONID=7&AJAX=AJAX-FALSE&CATALOGID=1110&TABKEY=tab5&tab5PAGENO=%s' % page_num
    s = requests.session()
    s.keep_alive = False
    r = None
    while r == None:
        try:
            r = s.get(url, timeout=3)
        except:
            pass
        else:
            pass
            #print('获取第%s页数据。' % page_num)
    html = r.content
    soup = BeautifulSoup(html, "html.parser")
    source = soup.select('tr[bgcolor="#ffffff"]')
    source1 = soup.select('tr[bgcolor="#F8F8F8"]')
    source += source1
    for l in source:
        code = l.a.u.text
        li.append(code)

def get_szcy_page(page_num):
    # print('获取第%s页数据。' % page_num)
    url = 'http://www.szse.cn/szseWeb/FrontController.szse?ACTIONID=7&AJAX=AJAX-FALSE&CATALOGID=1110&TABKEY=tab6&tab6PAGENO=%s' % page_num
    s = requests.session()
    s.keep_alive = False
    r = None
    while r == None:
        try:
            r = s.get(url, timeout=3)
        except:
            pass
        else:
            pass
            #print('获取第%s页数据。' % page_num)
    html = r.content
    soup = BeautifulSoup(html, "html.parser")
    source = soup.select('tr[bgcolor="#ffffff"]')
    source1 = soup.select('tr[bgcolor="#F8F8F8"]')
    source += source1
    for l in source:
        code = l.a.u.text
        li.append(code)


##############==============================================############
# 导入股票

def get_list(listname='share_list'):
    globals()[listname] = []
    get_sha_list()
    get_sza_list()
    get_szzx_list()
    get_szcy_list()
    globals()[listname] = list(set(globals()[listname]))
    print('一共导入 %s 支股票。' % len(globals()[listname]))


# 导入上海A股列表share_list并去除20171201以后上市的股票
def get_sha_list(listname='share_list', afterdate=20171201):
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
    li = []
    for i in range(len(stock_data)):
        code = stock_data[i]['SECURITY_CODE_A']
        listing_date = stock_data[i]['LISTING_DATE']
        if listing_date != '-':
            d = listing_date.split('-')
            n = int(d[0]+d[1]+d[2])
            if n < afterdate:
                globals()[listname].append(code)
                li.append(code)
        else: 
            globals()[listname].append(code)
            li.append(code)
    print('从 沪A 成功导入%s支股票。' % len(li))

# 导入深圳A股列表share_list并去除20171201以后上市的股票
def get_sza_list(listname='share_list', afterdate=20171201):
    global li
    if listname in globals().keys():
        if listname != 'share_list':
            globals()[listname] = []
    else:
        globals()[listname] = []
    index_url = 'http://www.szse.cn/szseWeb/FrontController.szse?ACTIONID=7&AJAX=AJAX-FALSE&CATALOGID=1110&TABKEY=tab2&tab2PAGENO=1'
    s = requests.session()
    s.keep_alive = False
    index_html = s.get(index_url).content
    index_soup = BeautifulSoup(index_html, "html.parser")
    index = int(index_soup.select('td')[-3].text.split()[1][1:-1])
    li = []
    threads = []
    print('正在获取深A列表，一共%s页。' % (index+1))
    for i in range(index):
        i = i + 1
        a = threading.Thread(target=get_sza_page, args=(i, afterdate,))
        threads.append(a)
        a.start()
    for t in threads:
        t.join()
    globals()[listname] += li
    print('从 深A 成功导入%s %s支股票。' % (listname, len(li)))

# 导入深圳中小板share_list
def get_szzx_list(listname='share_list'):
    global li
    if listname in globals().keys():
        if listname != 'share_list':
            globals()[listname] = []
    else:
        globals()[listname] = []
    index_url = 'http://www.szse.cn/szseWeb/FrontController.szse?ACTIONID=7&AJAX=AJAX-FALSE&CATALOGID=1110&TABKEY=tab5&tab5PAGENO=1'
    s = requests.session()
    s.keep_alive = False
    index_html = s.get(index_url).content
    index_soup = BeautifulSoup(index_html, "html.parser")
    index = int(index_soup.select('td')[-3].text.split()[1][1:-1])
    li = []
    threads = []
    print('正在获取深圳中小板列表，一共%s页。' % (index+1))
    for i in range(index):
        i = i + 1
        a = threading.Thread(target=get_szzx_page, args=(i,))
        threads.append(a)
        a.start()
    for t in threads:
        t.join()
    globals()[listname] += li
    print('从 深圳中小板 成功导入%s %s支股票。' % (listname, len(li)))

# 导入深圳创业板share_list
def get_szcy_list(listname='share_list'):
    global li
    if listname in globals().keys():
        if listname != 'share_list':
            globals()[listname] = []
    else:
        globals()[listname] = []
    index_url = 'http://www.szse.cn/szseWeb/FrontController.szse?ACTIONID=7&AJAX=AJAX-FALSE&CATALOGID=1110&TABKEY=tab6&tab6PAGENO=1'
    s = requests.session()
    s.keep_alive = False
    index_html = s.get(index_url).content
    index_soup = BeautifulSoup(index_html, "html.parser")
    index = int(index_soup.select('td')[-3].text.split()[1][1:-1])
    li = []
    threads = []
    print('正在获取深圳创业板列表，一共%s页。' % (index+1))
    for i in range(index):
        i = i + 1
        a = threading.Thread(target=get_szcy_page, args=(i,))
        threads.append(a)
        a.start()
    for t in threads:
        t.join()
    globals()[listname] += li
    print('从 深圳创业板 成功导入%s %s支股票。' % (listname, len(li)))

############################==================================##########################
###多线程筛选
def sort_list(listname='share_list', price=18, day=10):
    a = len(globals()[listname])
    sort_price_list(listname, price)
    sort_ma_list(listname, day)
    b = len(globals()[listname])
    print('过滤掉%s支股票，还剩%s支股票' % (a-b, b))

# 筛选价格
def sort_price(share_code, target_price=18):
    #print('检查 %s 价格是否低于%s元' % (share_code, target_price))
    price = price_now(share_code)[0]
    if price == '':
        li.remove(share_code)
        #print('%s 无法获取价格。' % share_code)
    elif price > target_price:
        li.remove(share_code)
        #print('%s 不符合条件。' % share_code)

def sort_price_list(listname='share_list', target_price=18):
    global li
    li = list(globals()[listname])
    threads = []
    print('筛选%s中，价格低于%s元, 一共%s支股票。' % (listname, target_price,len(globals()[listname])))
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

# 筛选MA
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

def sort_ma_list(listname='share_list', days=10):
    global li
    li = list(globals()[listname])
    threads = []
    print('筛选%s中MA10连续%s日大于MA5, 一共%s支股票。' % (listname, days, len(globals()[listname])))
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


###########################
def ma_monitor_start(listname='share_list', count=9999):
    global a
    a = threading.Thread(target=ma_monitor, args=())
    a.start()


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
    
    

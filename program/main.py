# !/Python

import requests
import sqlite3
import threading
import time
from bs4 import BeautifulSoup
from datetime import date
from datetime import datetime

############PROXY###########

proxies = {
    "https": "http://165.227.100.201:80",
    "https": "http://183.235.254.159:8080",
    "https": "http://183.235.254.159:8080"
}
proxies = None

########--Tools--########

#######---get-data---#######

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

############################=================sort==============##########################
# 多线程筛选
##########################################
# 监视程序
# 启动关闭MA监视
#watchdog


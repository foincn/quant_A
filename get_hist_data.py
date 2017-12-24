# !/Python

import get_ashare_list.py

import requests
import sqlite3
import threading
from multiprocessing import Process
import time

threads = []
for i in ashare_list:
    a = threading.Thread(target=get_ma_data, args=(i,))
    threads.append(a)
    a.start()

for t in threads:
    t.join()

print('FINISH')

counts = []
for i in ashare_list:
    b = Process(target=get_ma_data, args=(i,))
    counts.append(b)
    b.start()

for c in counts:
    c.join()


# 获取MA数据
def get_ma_hist(stock_code):
    print('Getting %s Data' % stock_code)
    s = requests.session()
    s.keep_alive = False
    url =  'http://api.finance.ifeng.com/akdaily/?code=%s&type=last' % sscode(stock_code)
    r = s.get(url, timeout=5)
    ma = r.json()['record']
    # MA5
    ma5_1 = float(ma[-2][8])
   # MA10
    ma10_1 = float(ma[-2][9])
    globals()['hist'+str(stock_code)] = (ma5_1, ma10_1)

for i in ashare_list:
    get_ma_hist(i)

def get_ma_now(stock_code):
    print('Getting %s Data' % stock_code)
    s = requests.session()
    s.keep_alive = False
    url =  'http://api.finance.ifeng.com/akdaily/?code=%s&type=last' % sscode(stock_code)
    r = s.get(url, timeout=5)
    ma = r.json()['record']
    # MA5
    ma5_now = float(ma[-1][8])
   # MA10
    ma10_now = float(ma[-1][9])
    globals()['now'+str(stock_code)] = [ma5_now, ma10_now]

buy_list = []

while Ture:
    get_ma_now(stock_code)
    if globals()['now'+str(stock_code)][0] > globals()['now'+str(stock_code)][1]:
        #inseart()
        buy_list.append(stock_code)
    time.sleep(15)
    



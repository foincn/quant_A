# !/Python

import get_ashare_list.py

import requests
import sqlite3
import threading
from multiprocessing import Process

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


# 获取MA历史数据
def get_ma_data(stock_code):
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
    globals()['dt'+str(stock_code)] = [ma5_1, ma5_2, ma10_1]

for i in ashare_list:
    get_ma_data(i)


    

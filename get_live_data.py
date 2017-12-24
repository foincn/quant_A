# !/Python

import get_ashare_list.py
import get_hist_data.py

import requests
import sqlite3
import threading

def get_ma_now(stock_code):
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

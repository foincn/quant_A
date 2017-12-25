# !/Python

import get_ashare_list.py
import get_hist_data.py

import requests
import sqlite3
import threading
from datetime import date

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
    ma = s.get(url, timeout=3)
    ma_data = ma.text.split('[')[1].split(']')[0].split(',')
    ma5 = float(ma_data[0])
    ma10 = float(ma_data[1])
    ma20 = float(ma_data[2])
    return(ma5, ma10)

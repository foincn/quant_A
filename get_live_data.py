# !/Python

import get_ashare_list.py
import get_hist_data.py

import requests
import sqlite3
import threading

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

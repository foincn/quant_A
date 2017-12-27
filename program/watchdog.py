# !/Python

# 监视程序
# 启动关闭MA监视
def ma_monitor_start(listname='share_list', count=9999):
    global a
    a = threading.Thread(target=ma_monitor, args=())
    a.start()

def ma_monitor_stop():
    globals()['ma_monitor_status'] = True
    print('监视结束！')

# MA监视循环
def ma_monitor(listname='share_list', count=9999):
    global buy_list
    global ma_monitor_status
    ma_monitor_status = False
    buy_list = []
    create_ma_form('MA')
    c = 0
    print('开始扫描，一共%s次。' % count)
    start_time = datetime.now()
    while c < count:
        while ma_monitor_status != True:
            c += 1
            # time.sleep(10)
            for i in globals()[listname]:
                ma_checker(i)
            end_time = datetime.now()
            timedelsta = (end_time - start_time).seconds
            print('第%s次扫描完成, 一共%s支股票，已找到%s支股票符合。 本次扫描耗时%s秒。' % (c, len(globals()[listname]), len(buy_list), timedelsta))
            start_time = end_time

# Ma监视条件
def ma_checker(stock_code):
    ma = ma_now(stock_code)
    if ma[0] > ma[1]:
        if ma[0] > globals()['ma'+stock_code][0] and  ma[1] > globals()['ma'+stock_code][1]:
            if stock_code not in buy_list:
                buy_list.append(stock_code)
                print('%s买入时机' % stock_code)
                insert_ma_data(stock_code, ma)

# 在数据库'MA'中建立表 '17-12-27'/ CODE/ NAME/ PRICE/ AVERAGE/ TIME/ TIMECROSS/ OTHER
def create_ma_form(dbname):
    date = datetime.now().strftime('\"%y-%m-%d\"')
    conn = sqlite3.connect('database/%s.db' % dbname)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS %s
        (CODE TEXT PRIMARY KEY UNIQUE,
        NAME   TEXT,
        PRICE  TEXT,
        AVERAGE  TEXT,
        MA5  TEXT,
        MA10  TEXT,
        TIME   TEXT,
        TIMECROSS   TEXT,
        OTHER   TEXT);''' % date)
    conn.commit()
    conn.close()
    print("Form %s Created in %s!" % (date, dbname))

# 在数据库'MA'，表'17-12-27'中 写入 / CODE/ NAME/ PRICE/ AVERAGE/ TIME/
def insert_ma_data(stock_code, ma_now):
    prices = price_now(stock_code)
    price = str(prices[0])
    average = str(prices[1])
    name = share_name(stock_code)
    ma5 = ma_now[0]
    ma10 = ma_now[1]
    time = datetime.now().strftime('%H:%M:%S')
    formname = datetime.now().strftime('\"%y-%m-%d\"')
    conn = sqlite3.connect('database/MA.db')
    c = conn.cursor()
    print(stock_code, name, price, average, time)
    c.execute("INSERT OR IGNORE INTO %s (CODE, NAME, PRICE, AVERAGE, MA5, MA10, TIME) VALUES (?, ?, ?, ?, ?, ?, ?)" % formname,(stock_code, name, price, average, ma5, ma10, time))
    conn.commit()
    conn.close()
    print('写入 %s 数据成功！' % stock_code)


if __name__ != '__main__':
    print('''
    ma_monitor_start(listname='share_list', count=9999)
    ma_monitor_stop()
    ''')
    
    
    
    

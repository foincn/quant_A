# !/Python

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
        print('%s 无法获取价格。' % share_code)
    elif price > target_price:
        li.remove(share_code)
        print('%s 不符合条件。' % share_code)
    else:
        print('%s 符合条件!' % share_code)

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



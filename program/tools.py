# !/Python

########--Tools--########

# 股票代码
def sscode(code):
    code = str(code)
    if code[0]+code[1] =='60':
        code = 'sh%s' % code
    else:
        code = 'sz%s' % code
    return code


# 股票名
def share_name(code):
    s = requests.session()
    s.keep_alive = False
    url = 'http://hq.sinajs.cn/list=%s' % sscode(code)
    r = None
    while r == None:
        r = s.get(url, timeout=2)
    name = r.text.split("\"")[1].split(",",1)[0]
    return name


# 现价／均价
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


# 最新 MA5／MA10
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


# MA5/MA10 历史按天
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



# !/Python

########--Tools--########

# sh600001/sz000001
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



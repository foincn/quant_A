import requests


payload = {
    
r = requests.post()



def get_sza_list():
    s = requests.session()
    s.keep_alive = False
    index_url = 'http://www.szse.cn/szseWeb/FrontController.szse?ACTIONID=7&AJAX=AJAX-FALSE&CATALOGID=1110&TABKEY=tab2&tab2PAGENO=1'
    index_html = s.get(index_url).content
    index_soup = BeautifulSoup(index_html, "html.parser")
    index = int(index_soup.select('td')[-3].text[-4:-1])
    threads = []
    for i in range(index):
        a = threading.Thread(target=sza_page, args=(i,))
        a.start()
    for t in threads:
        t.join()

def sza_page(ind):
    ind = ind + 1
    print('获取第%s页数据。' % ind)
    url = 'http://www.szse.cn/szseWeb/FrontController.szse?ACTIONID=7&AJAX=AJAX-FALSE&CATALOGID=1110&TABKEY=tab2&tab2PAGENO=%s' % ind
    html = s.get(url).content
    soup = BeautifulSoup(html, "html.parser")
    source = soup.select('tr[bgcolor="#ffffff"]')
    source1 = soup.select('tr[bgcolor="#F8F8F8"]')
    source += source1
    for l in source:
        code = l.select('td')[2].text
        print(code)
        listing_date = l.select('td')[4].text
        print(listing_date)
        if listing_date != '-':
            d = listing_date.split('-')
            n = int(d[0]+d[1]+d[2])
            if n < 20171201:
                ashare_list.append(code)
                print('%s Added!' % code)
        else: 
            ashare_list.append(code)
            print('%s Added!' % code)





                
                

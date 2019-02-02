import requests
from bs4 import BeautifulSoup
import spider

HTTPS_API = 'http://www.xiladaili.com/https/'

soup = BeautifulSoup(spider.gethtml(HTTPS_API), 'html.parser')

trs = soup.findAll('table')[0].find('tbody').findAll('tr')
for tr in trs:
    tds = tr.findAll('td')
    proxyhttps = 'https://' + tds[0].text

    spider.proxyDict["https"] = proxyhttps

    try:
        res = requests.get(spider.HTTPS_URL, proxies=spider.proxyDict, timeout=10)
        if res.status_code == 200:
            print proxyhttps
    except Exception as err:
        print err


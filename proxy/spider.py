from bs4 import BeautifulSoup
import threading
import requests
import ipbean

threads = []
url = 'https://www.xicidaili.com/wt/'
HTTP_URL = 'http://asche.top'
HTTPS_URL = 'https://www.baidu.com/'
proxyDict = {
              "http": '',
              "https": '',
              "ftp": ''
            }

# res = requests.get(HTTP_URL, proxies=proxyDict)
# print res.content


class CheckIP(threading.Thread):
    def __init__(self, obj):
        threading.Thread.__init__(self)
        self.obj = obj

    def run(self):
        if check(self.obj):
            print self.obj.getstr()
            ipbean.insert(self.obj)


def gethtml(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
    res = requests.get(url, headers=headers)
    return res.content


def check(bean):
    ipproxy = bean.getstr()
    proxyDict["http"] = ipproxy
    proxyDict["https"] = ipproxy
    try:
        res = requests.get(HTTP_URL, proxies=proxyDict, timeout=5)
        resp = requests.get(HTTPS_URL, proxies=proxyDict, timeout=5)
        if res.status_code == 200 & resp.status_code == 200:
            return True
        else:
            return False
    except:
        return False


def parsehtml(url):
    soup = BeautifulSoup(gethtml(url), 'html.parser')

    tags = soup.findAll('tr')
    tags.pop(0)
    for tag in tags:
        trs = tag.findAll('td')
        ip = trs[1].text
        port = trs[2].text
        print ip, port

        bean = ipbean.IPBean(ip, port)

        thread = CheckIP(bean)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    global threads
    threads = []


def save():
    file_ = open('iplist_http.txt', 'w')
    for bean in ipbean.lists:
        file_.write(bean.getstr() + '\n')
    file_.close()


def start():
    for i in range(5):
        parsehtml(url + str(i + 1))

    print 'Total ip num:', len(ipbean.lists)
    save()


if __name__ == '__main__':
    start()


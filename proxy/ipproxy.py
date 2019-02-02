import random
import spider
import requests

# save proxy str such as 'http://119.101.125.231:9999'
lists = []


def read():
    file_ = open('iplist_http.txt', 'r')
    for line in file_:
        # print line
        lists.append(line[:-1])


def gethttpproxy():
    if len(lists) == 0:
        read()
        if len(lists) == 0:
            spider.start()
        read()
    return lists[random.randint(0, len(lists)-1)]


# read()
# print lists
if __name__ == '__main__':

    for i in range(10):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

            proxystr = gethttpproxy()
            spider.proxyDict["http"] = proxystr
            spider.proxyDict["https"] = proxystr
            print proxystr

            res = requests.get('http://asche.top', headers=headers, timeout=10, proxies=spider.proxyDict)
            # print res.content
            print 'Succeed!'
            res.close()
        except Exception as error:
            print error


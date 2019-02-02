
import random
from threading import Lock


lists = []


class IPBean:
    # type ---> HTTP: 0; HTTPS: 1
    def __init__(self, ip, port, proxytype = 0):
        self.ip = ip
        self.port = port
        self.proxytype = proxytype

    def getstr(self):
        if self.proxytype == 0:
            return 'http://{0}:{1}'.format(self.ip, self.port)
        else:
            return 'https://{0}:{1}'.format(self.ip, self.port)


# add lock operation
def insert(obj):
    lock = Lock()
    lock.acquire()
    lists.append(obj)
    lock.release()


# get a ip proxy object
def getipbean():
    size = len(lists)
    print size
    if size != 0:
        return lists[random.randint(0, size-1)]


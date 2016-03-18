import urllib
import time
from datetime import date

proxies = {'ftp': 'http://10.144.1.10:8080/'}


# url = 'http://home.baidu.com/2016-03-01/1464746500.html'
# f = 'd:/tmp/baidu.html'

def download(fileCode):
    url = 'ftp://115.29.204.48/webdata/{}.xls'.format(fileCode)
    f = 'd:/tmp/auto-download/{}_{}.xls'.format(fileCode, date.today())
    testfile = urllib.FancyURLopener(proxies)
    print 'start download ' + url + '...'
    testfile.retrieve(url, f)
    print f + ' saved'

download('Csi300Perf')
download('Csi905Perf')

print 'download complete, exit within 5 seconds'
time.sleep(5)

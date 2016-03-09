import urllib
from datetime import date

proxies = {'ftp': 'http://192.0.1.1:8080/'}
# url = 'http://home.baidu.com/2016-03-01/1464746500.html'
# f = 'd:/tmp/baidu.html'
url = 'ftp://115.29.204.48/webdata/Csi300Perf.xls'
f = 'd:/tmp/auto-download/Csi300Perf_{}.xls'.format(date.today())
testfile = urllib.FancyURLopener(proxies)
print 'start download ' + url + '...'
testfile.retrieve(url, f)
print f + ' saved'

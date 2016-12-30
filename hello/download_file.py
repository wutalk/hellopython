import urllib
import time
from datetime import date

proxies = {'ftp': 'http://10.144.1.10:8080/'}


# url = 'http://home.baidu.com/2016-03-01/1464746500.html'
# f = 'd:/tmp/baidu.html'

def download(fileCode):
    url = 'ftp://115.29.204.48/webdata/{}.xls'.format(fileCode)
    f = 'D:/wutalk/portfolio/perf_data/{}_{}.xls'.format(fileCode, date.today())
    testfile = urllib.FancyURLopener(proxies)
    print 'start download ' + url + '...'
    testfile.retrieve(url, f)
    print 'saved to ' + f

# 上证50 '000016.XSHG', 红利指数 '000015.XSHG', 中证红利 '000922.XSHG', 
# 基本面50 '000925.XSHG', '000300.XSHG', '000905.XSHG'
download('000015perf')
download('000016perf')
download('Csi922Perf')
download('Csi925Perf')
download('Csi300Perf')
download('Csi905Perf')

print 'download complete, exit within 2 seconds'
time.sleep(2)

import urllib
import urllib2
from bs4 import BeautifulSoup

url = 'http://home.baidu.com/2016-03-01/1464746500.html'
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
values = {'name': 'Michael Foord',
          'location': 'Northampton',
          'language': 'Python'}
headers = {'User-Agent': user_agent}

data = urllib.urlencode(values)
req = urllib2.Request(url, data, headers)
response = urllib2.urlopen(req)
the_page = response.read()
response.close()

html = unicode(the_page, 'gbk')#.encode('utf-8')
soup = BeautifulSoup(html, "html.parser")
# print html
print(soup.title.string)



print('end')
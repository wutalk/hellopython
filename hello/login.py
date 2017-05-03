import cookielib
import urllib
import urllib2
from bs4 import BeautifulSoup

username = 'wu_yaowen@163.com'
password = 'yourpwd'

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
login_data = urllib.urlencode({'command': 'login', 'username': username, 'password': password})
login_res = opener.open('https://cn.morningstar.com/handler/authentication.ashx', login_data)
content = str(login_res.read())
print content
if content.startswith('Success'):
    print 'logged in'
    resp = opener.open('https://cn.morningstar.com/client/portfolio/holding-20301')
    the_page = resp.read()
    html = unicode(the_page, 'gbk')  # .encode('utf-8')
    soup = BeautifulSoup(html, "html.parser")
    # print html
    print(soup.title.string)
print 'job is done'

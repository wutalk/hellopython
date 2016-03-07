import os

print os.getcwd()
print os.name
# for k, v in os.environ.iteritems():
# print k + '=' + v

print dir(os)
# print help(os)

import shutil

shutil.copyfile('d:/tmp/test.log.2', 'd:/tmp/test.log')
# shutil.move('d:/tmp/test.log','d:/')

# parse html
# f = open('D:/tmp/about_baidu.html', 'r')
f = open('D:/tmp/csi_price.html', 'r')
html_str = f.read()
f.close()
html_str = unicode(html_str, 'gbk')

#print html_str

from bs4 import BeautifulSoup
soup = BeautifulSoup(html_str, 'html.parser')
print soup.title
print soup.find_all('div', attrs={"class": "f16b"})[0].text


from bs4 import BeautifulSoup

f = open('D:/tmp/ms-p-203.html', 'r')
html = f.read()
f.close()
# html = unicode(html, 'gbk')
soup = BeautifulSoup(html, "html.parser")
# print html
print(soup.title.string)
print(soup.body.string)

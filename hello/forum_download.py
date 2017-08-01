import codecs
import cookielib
import urllib2

from bs4 import BeautifulSoup

tmp_dir = 'D:/tmp/'
host = 'http://www.ishuiku.com/'
page_link = 'forum-97-2.html'
thread_link = 'thread-100364-1-4.html'


def download_file():
    print 'start download file'
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    resp = opener.open(host + page_link)
    print resp.headers['content-type']
    the_page = resp.read()
    html = unicode(the_page, 'utf-8')  # .encode('utf-8')
    # print html
    # with open(tmp_dir + "forum-97-4.html", "w") as pom_file:
    #     pom_file.write(html)
    with codecs.open(tmp_dir + page_link, "w", "utf-8") as temp:
        temp.write(html)


# download_file()

# list page
html_page = open(tmp_dir + page_link, 'r')
# print html_page
soup = BeautifulSoup(html_page, "html.parser")
print(soup.title.string)

thread_list = soup.select('#threadlisttableid th.new')
print len(thread_list)
for thread in thread_list:
    title = thread.select_one('a:nth-of-type(2)').get_text()
    print title
    link = thread.select_one('a:nth-of-type(2)').get('href')
    print link

print 'job is done'
print host + page_link

# single page
html_page = open(tmp_dir + thread_link, 'r')
# print html_page
soup = BeautifulSoup(html_page, "html.parser")
# print(soup.title.string)

subject = soup.select_one('#thread_subject').get_text()
post_date = soup.select_one('em[id^=authorposton]').get_text()
author = soup.select_one('div.authi a').get_text()
# content = soup.select_one('td[id^=postmessage_]').get_text()
print subject
print author + ' ' + post_date
# print content

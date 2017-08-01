import codecs
import cookielib
import urllib2

import time
from bs4 import BeautifulSoup

tmp_dir = 'D:/tmp/ishuiku/'
host = 'http://www.ishuiku.com/'
list_page_template = 'forum-97-{idx}.html'
result_file = 'ishuiku-11-20.txt'

for i in range(12, 21):
    time.sleep(0.5)
    page_link = list_page_template.replace('{idx}', str(i))
    print 'processing ' + page_link

    # print 'start download file'
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    resp = opener.open(host + page_link)
    # print resp.headers['content-type']
    the_page = resp.read()
    article_page = unicode(the_page, 'utf-8')

    # print html_page
    soup = BeautifulSoup(article_page, "html.parser")
    print(soup.title.string)

    thread_list = soup.select('#threadlisttableid th.new')
    # print len(thread_list)
    for thread in thread_list:
        # time.sleep(0.2)
        title = thread.select_one('a:nth-of-type(2)').get_text()
        # print title
        link = thread.select_one('a:nth-of-type(2)').get('href')
        # print link

        print 'processing article: ' + title
        resp = opener.open(host + link)
        the_page = resp.read()
        article_page = unicode(the_page, 'utf-8')

        # print html_page
        soup = BeautifulSoup(article_page, "html.parser")

        subject = soup.select_one('#thread_subject').get_text()
        post_date = soup.select_one('em[id^=authorposton]').get_text()
        author = soup.select_one('div.authi a').get_text()
        content = soup.select_one('td[id^=postmessage_]').get_text()
        with codecs.open(tmp_dir + result_file, "a", "utf-8") as temp:
            temp.write('==================================\r\n')
            temp.write(subject + '\r\n')
            temp.write(author + ' ' + post_date + '\r\n')
            temp.write(content)
            temp.write('\r\n\r\n\r\n\r\n')
        # break

print 'job is done'

import codecs
import cookielib
import urllib2
import time

from bs4 import BeautifulSoup

tmp_dir = 'D:/data/lianjia/cq/'

# not chewei: not park-slot: hu1
# no shangye: not commercial: ng1
# dp1 is shangpin fang
base_url = 'https://cq.lianjia.com/ershoufang/%s/ng1hu1dp1'  # jiangbei/


# page = 'pg1'
# "i am a %s" % sub1

def download_file(sec):
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    page_url = base_url % sec
    print 'start download file: %s' % page_url
    # page_url = "http://home.baidu.com/home/index/news_detail/id/17786"
    resp = opener.open(page_url)
    print resp.headers['content-type']
    the_page = resp.read()
    html = unicode(the_page, 'utf-8')  # .encode('utf-8')
    print html
    # with open(tmp_dir + "forum-97-4.html", "w") as pom_file:
    #     pom_file.write(html)
    if sec == "":
        sec = "cq"
    with codecs.open(tmp_dir + sec + ".html", "w", "utf-8") as temp:
        temp.write(html)


def get_link_list(root_soup):
    link_list = []
    quyu = root_soup.find_all('div', attrs={"data-role": "ershoufang"})
    quyu_list = quyu[0].select('a')
    print len(quyu_list)
    for link in quyu_list:
        # print link.get('href')
        link_list.append((link.get('href'), link.get_text()))
    return link_list


if __name__ == '__main__':
    # download_file("")
    # download_file("jiangbei")
    # exit(0)

    page = tmp_dir + "cq.html"

    html_page = open(page, 'r')
    # print html_page
    soup = BeautifulSoup(html_page, "html.parser")
    print soup.title.string

    lk_list = get_link_list(soup)
    # for lk in lk_list:
    #     print lk[1] + lk[0]

    line_list = soup.select('div.list-more dl')
    print len(line_list)
    item_return = []
    i = 1
    for line in line_list:
        # print line.get_text()
        print '------------'
        print line.select_one('dt').get_text()
        item_list = line.select('a')
        print "sub item %s" % len(item_list)
        for item in item_list:
            name = item.select_one('span.name').get_text()
            cnt = item.select_one('span.cnt').get_text()
            item_return.append((name, cnt))
            print name, cnt
        print i
        if ++i > 2:
            break
    # print item_return.join(', ')
    print 'end'

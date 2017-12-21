import codecs
import cookielib
import urllib2

import pandas as pd
from bs4 import BeautifulSoup

tmp_dir = 'D:/tmp/cdfgj-data/'

base_url = 'http://www.cdfgj.gov.cn/SCXX/Default.aspx'


def download_file():
    print 'start download file'
    today = pd.datetime.today()
    today = today.strftime('%Y-%m-%d')
    # example cdfgj_cj_2017-12-20.html
    page = 'cdfgj_cj_' + today + ".html"
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    resp = opener.open(base_url)
    print resp.headers['content-type']
    the_page = resp.read()
    html = unicode(the_page, 'utf-8')  # .encode('utf-8')
    # print html
    with codecs.open(tmp_dir + page, "w", "utf-8") as temp:
        temp.write(html)


def parse_page(page):
    page_path = tmp_dir + page

    html_page = open(page_path, 'r')
    soup = BeautifulSoup(html_page, "html.parser")
    # print(soup.title.string)

    house_list = soup.select('div.rightContent > table')
    print len(house_list)

    for line in parse_table(house_list[0]):
        print line
    print '--------------'
    for line in parse_table(house_list[1]):
        print line


def parse_table(ershou):
    es_lines = []
    es_list = ershou.select('table')[1].select('tr')
    for i in range(2, len(es_list)):
        line_item = es_list[i].select('td')
        line = []
        for j in range(len(line_item)):
            line.append(line_item[j].get_text().strip())
        # print ','.join(line)
        es_lines.append(','.join(line))
    return es_lines


if __name__ == '__main__':
    # exit(0)
    download_file()
    page = 'cdfgj_cj_2017-12-20 .html'
    parse_page(page)
    print 'page processed'

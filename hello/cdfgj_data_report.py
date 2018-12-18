import codecs
import cookielib
import urllib2
import os.path

import pandas as pd
from bs4 import BeautifulSoup

tmp_dir = 'D:/data/cdfgj-data/'

base_url = 'http://www.cdfgj.gov.cn/SCXX/Default.aspx'

page = ""


def download_file():
    print 'start download file from %s' % base_url
    today = pd.datetime.today()
    today = today.strftime('%Y-%m-%d')
    # example cdfgj_cj_2017-12-20.html
    save_page = 'cdfgj_cj_' + today + ".html"
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    resp = opener.open(base_url)
    print resp.headers['content-type']
    the_page = resp.read()
    html = unicode(the_page, 'utf-8')  # .encode('utf-8')
    # print html
    with codecs.open(tmp_dir + save_page, "w", "utf-8") as temp:
        temp.write(html)
    print 'downloaded %s' % save_page
    return save_page


def parse_page(page):
    page_path = tmp_dir + page

    html_page = open(page_path, 'r')
    soup = BeautifulSoup(html_page, "html.parser")
    # print(soup.title.string)

    house_list = soup.select('div.rightContent > table')
    print len(house_list)

    print '------yishou--------'
    data_list = []
    for line in parse_table(house_list[0], 'yishou'):
        print line
        data_list.append(line)
    print '------ershou--------'
    for line in parse_table(house_list[1], 'ershou'):
        print line
        data_list.append(line)
    return data_list


def parse_table(house_list, new_ershou):
    es_lines = []
    es_list = house_list.select('table')[1].select('tr')
    for i in range(2, len(es_list)):
        line_item = es_list[i].select('td')
        today = pd.datetime.today()
        today = today.strftime('%Y-%m-%d')
        line = [today, new_ershou]
        for j in range(len(line_item)):
            line.append(line_item[j].get_text().strip())
        # print ','.join(line)
        es_lines.append(','.join(line))
    return es_lines


def append_to_file(data_list):
    print 'start write to file'
    out_file = tmp_dir + "cdfgj_cj_data.csv"
    with codecs.open(out_file, "a", "utf-8") as f:
        for line in data_list:
            # print line
            f.write(line)
            f.write('\r\n')
    print 'complete append %s lines to file' % len(data_list)


if __name__ == '__main__':
    # exit(0)
    page = download_file()
    if not os.path.isfile(tmp_dir + page):
        print 'download file fail, retry one'
        page = download_file()
    # page = 'cdfgj_cj_2018-05-15.html'
    item_list = parse_page(page)
    print 'processed %s' % page
    append_to_file(item_list)

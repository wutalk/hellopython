import codecs
import cookielib
import os.path
import urllib2

import pandas as pd
from bs4 import BeautifulSoup

tmp_dir = 'D:/data/cdfgj-data/'

# base_url = 'http://www.cdfgj.gov.cn/SCXX/Default.aspx'
# base_url = 'http://fgj.chengdu.gov.cn/cdsfgj/jsjy/jsjy.shtml'
# base_url = 'https://www.cdfgj.gov.cn/SCXX/Default.aspx?action=ucEveryday'
base_url = 'https://zw.cdzj.chengdu.gov.cn/py/SCXX/Default.aspx?action=ucEveryday'

page = ""


def download_file():
    print 'start download file from %s' % base_url
    today = pd.datetime.today()
    today = today.strftime('%Y-%m-%d')
    # example cdfgj_cj_2017-12-20.html
    save_page = 'cdfgj_cj_' + today + ".html"
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    opener.addheaders = [('User-Agent',
                          'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'),
                         ('Accept',
                          'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3')]
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
    date_str = get_date_from_page_name(page)

    html_page = open(page_path, 'r')
    soup = BeautifulSoup(html_page, "html.parser")
    # print(soup.title.string)
    # print soup

    house_list = soup.select('div.rightContent > table')
    print len(house_list)

    print '------yishou--------'
    data_list = []
    for line in parse_table(house_list[0], 'yishou', date_str):
        print line
        data_list.append(line)
    print '------ershou--------'
    for line in parse_table(house_list[1], 'ershou', date_str):
        print line
        data_list.append(line)
    return data_list


def parse_table(house_list, new_ershou, date_str):
    es_lines = []
    es_list = house_list.select('table')[1].select('tr')
    for i in range(2, len(es_list)):
        line_item = es_list[i].select('td')
        # today = pd.datetime.today()
        # today = today.strftime('%Y-%m-%d')
        today = date_str
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


def get_date_from_page_name(page):
    items = page.split('_')
    data_str = items[2]
    return data_str.split('.')[0]


if __name__ == '__main__':
    # exit(0)
    page = download_file()
    if not os.path.isfile(tmp_dir + page):
        print 'download file fail, retry one'
        page = download_file()
    # page = 'cdfgj_cj_2019-02-22.html'
    item_list = parse_page(page)
    print 'processed %s' % page
    append_to_file(item_list)

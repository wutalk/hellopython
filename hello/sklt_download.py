import codecs
import cookielib
import os
import urllib2

import pandas as pd
from bs4 import BeautifulSoup

tmp_dir = 'D:/data/sklt/'

base_url = 'https://mp.weixin.qq.com/s?__biz=MzAxNTMxMTc0MA==&mid=401338731&idx=1&sn=afb1238dc2b229f0ccfc71915a07d039&scene=21#wechat_redirect'
page_sn = base_url.split("&")[3].split("=")[1]
page = ""


def download_file():
    print 'start download file from %s' % base_url
    save_page = 'sknt_' + page_sn + ".html"
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

    print "start parse %s" % page_path
    html_page = open(page_path, 'r')
    soup = BeautifulSoup(html_page, "html.parser")
    print(soup.title.string.strip())

    images = soup.find("div", {"id": "img-content"}).select("img[data-src]")
    print len(images)

    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    for img in images:
        url = img["data-src"]
        # print url
        img_name = str(url).split('/')[4] + ".png"
        print 'start download %s' % img_name
        resp = opener.open(url)
        the_page = resp.read()
        img_dir = tmp_dir + page_sn
        create_dir(img_dir)
        img_path = img_dir + "/" + img_name
        # print img_path
        with codecs.open(img_path, "wb") as temp:
            temp.write(the_page)
        print 'downloaded %s' % img_name


def create_dir(path):
    if not os.path.isdir(path):
        try:
            os.mkdir(path)
        except OSError:
            print ("Creation of the directory %s failed" % path)
        else:
            print ("Successfully created the directory %s " % path)


def replace_page_images(page):
    img_dir = page.split(".")[0]

if __name__ == '__main__':
    # exit(0)
    # page = download_file()
    # if not os.path.isfile(tmp_dir + page):
    #     print 'download file fail, retry one'
    #     page = download_file()
    page = 'afb1238dc2b229f0ccfc71915a07d039.html'
    parse_page(page)
    replace_page_images(page)
    # print 'processed %s' % page
    # append_to_file(item_list)

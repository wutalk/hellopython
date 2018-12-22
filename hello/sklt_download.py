# -*- coding=utf-8 -*-
import codecs
import cookielib
import os
import time
import urllib2

from bs4 import BeautifulSoup

tmp_dir = 'D:/data/sklt/'


def download_file(base_url):
    print 'downloading from %s' % base_url
    the_page = do_download(base_url)
    html_file = unicode(the_page, 'utf-8')  # .encode('utf-8')
    # print html_file
    soup = BeautifulSoup(html_file, "html.parser")

    page_sn = get_page_sn(base_url)
    save_page = page_sn + ".html"

    soup = parse_page(soup, page_sn)

    with codecs.open(tmp_dir + save_page, "w", "utf-8") as temp:
        temp.write(soup.prettify(formatter="html"))
    print 'downloaded %s' % save_page
    return save_page


def do_download(base_url):
    for i in range(3):
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        try:
            resp = opener.open(base_url)
            # print resp.headers['content-type']
            the_page = resp.read()
            return the_page
        except urllib2.URLError, err:
            print 'fail to open link: %s' % base_url
            print(str(err))
            time.sleep(5)
        finally:
            try:
                if resp:
                    resp.close()
            except err:
                print 'fail to close'
                pass


def parse_page_local(page, page_sn):
    page_path = tmp_dir + page
    print "start parse %s" % page_path
    # html_file = open(page_path, 'r')
    with open(page_path, 'r+') as html_file:
        soup = BeautifulSoup(html_file, "html.parser")
        soup = parse_page(soup, page_sn)
        # with codecs.open(page_path, "w", "utf-8") as temp:
        #     temp.write(soup.prettify(formatter="html"))
        #     print 'page saved with image'
        # write back image updated
        html_file.seek(0)
        html_file.write(soup.prettify(formatter="html"))
        html_file.truncate()
        print 'page saved with image'


def parse_page(soup, page_sn):
    # soup = BeautifulSoup(html_file, "html.parser")
    valid_page = soup.select_one("#img-content")
    if not valid_page:
        print "page is deleted: " + page_sn
        return soup

    title_str = soup.title.string
    if title_str:
        title = title_str.strip()
        # print(title)

    images = soup.select_one("#img-content").select("img[data-src]")
    # print len(images)
    if len(images) > 0:
        img_dir = tmp_dir + page_sn
        create_dir(img_dir)
        for img in images:
            url = img["data-src"]
            # print url
            img_name = str(url).split('/')[4] + ".png"

            # print 'start download %s' % img_name
            the_page = do_download(url)
            # print 'downloaded %s' % img_name

            img_path = img_dir + "/" + img_name
            # print img_path
            with codecs.open(img_path, "wb") as temp:
                temp.write(the_page)

            img['src'] = page_sn + '/' + img_name
            # print img
    print 'downloaded images: %s' % len(images)

    return soup
    # print 'save page with image'
    # with codecs.open(tmp_dir + title + '.html', "w", "utf-8") as temp:
    # with codecs.open(page_path, "w", "utf-8") as temp:
    #     temp.write(soup.prettify(formatter="html"))
    #     print 'page saved with image'
    # write back image updated
    # html_file.seek(0)
    # html_file.write(soup.prettify(formatter="html"))
    # html_file.truncate()
    # print 'page saved with image'


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
    imgs = os.listdir(tmp_dir + img_dir)

    # for img in imgs:
    # print img
    print "start replace %s" % page
    page_path = tmp_dir + page
    html_page = open(page_path, 'r')
    soup = BeautifulSoup(html_page, "html.parser", from_encoding="utf-8")
    print(soup.title.string.strip())

    images = soup.select_one("#img-content").select("img[data-src]")
    print len(images)
    for img in images:
        url = img["data-src"]
        img_name = str(url).split('/')[4] + ".png"
        img['src'] = img_dir + '/' + img_name
        # print img
    saved = tmp_dir + "bk_" + page
    with codecs.open(page_path, "w", "utf-8") as temp:
        temp.write(soup.prettify(formatter="html"))


def parse_index(idx_page):
    page_path = tmp_dir + idx_page
    # html_page = open(page_path, 'r')
    with codecs.open(page_path, "r", "utf-8") as html_page:
        soup = BeautifulSoup(html_page, "html.parser", from_encoding="utf-8")
        print(soup.title.string.strip())

        # sn_set = Set()
        article_list = soup.select_one("#img-content").select("a[href^=http]")
        print len(article_list)
        i = 0
        for item in article_list:
            i += 1
            # if i > 310:
            #     break
            sub_link = item['href']

            sn = get_page_sn(sub_link)
            # if sn not in sn_set:
            #     sn_set.add(sn)
            # else:
            #     print 'duplicate sn %s' % sn
            #     print 'page is %s' % item.get_text()
            # continue
            sub_page = sn + '.html'
            text = item.get_text()
            if os.path.isfile(tmp_dir + sub_page):
                print str(i) + ' >>> exists, skip download %s' % text
                continue
            print str(i) + ' >>> downloading ' + text
            page = download_file(sub_link)
            # parse_page(page, get_page_sn(sub_link))
            if i % 5 == 0:
                print 'sleep a while...'
                time.sleep(3)
                # print 'sn_set size %s' % str(len(sn_set))


def get_page_sn(pg_url):
    items = pg_url.split("&")
    # print items
    if len(items) >= 4:
        return items[3].split("=")[1]
    else:
        items = pg_url.split("/")
        return items[4]


def download_from_url_list():
    with codecs.open('D:/data/sklt/sklt-res-hidden-url-list.txt', "r", "utf-8") as hidden_list:
        i = 0
        for line in hidden_list:
            i += 1
            # if i > 30:
            #     break
            url = line.strip()
            # print url
            if len(url) == 0:
                print str(i) + ' >>> url is empty'
                continue

            sn = get_page_sn(url)
            sub_page = sn + '.html'
            if os.path.isfile(tmp_dir + sub_page):
                print str(i) + ' >>> exists, skip download %s' % sub_page
                continue
            print str(i) + ' >>> downloading ' + sub_page
            download_file(url)
            if i % 5 == 0:
                print 'sleep a while...'
                time.sleep(3)


def update_index(idx_page):
    mydict = prepare_soap_from_url_list()
    mykeys = mydict.keys()
    # print mykeys
    # return
    page_path = tmp_dir + idx_page
    # html_page = open(page_path, 'r')
    with codecs.open(page_path, "r+", "utf-8") as html_page:
        soup = BeautifulSoup(html_page, "html.parser", from_encoding="utf-8")
        # print(soup.title.string.strip())

        # sn_set = Set()
        ul_list = soup.select_one("#js_content").select("ul.list-paddingleft-2")
        print 'got parts: %s ' % len(ul_list)
        idx = 0
        for ul in ul_list:
            idx += 1
            li_list = ul.select('li h1')
            print 'got li: %s ' % len(li_list)
            for li in li_list:
                has_a = li.select('a')
                if len(has_a) == 0:
                    txt = li.get_text()
                    items = txt.split('#')
                    if len(items) == 2:
                        print items[0].strip() + '--' + items[1]
                        txt_no = items[1].strip()

                        for k in mykeys:
                            # print k, txt_no
                            # print type(k), type(txt_no)
                            if k == txt_no:
                                print '******* got you *** ' + txt_no
                                print k
                                print mydict.get(k)
                                asoap = BeautifulSoup(str(mydict.get(k)), "html.parser")
                                print li
                                li.clear()
                                print li
                                li.append(asoap.a)
                                print li
                                break
                                # else:
                                # print '-------------notfound'
                        continue
                    else:
                        print "***** invalid item " + li.get_text()
                        # if idx > 5:
                        #     break
        html_page.seek(0)
        html_page.write(soup.prettify(formatter="html"))
        html_page.truncate()
        print 'updated index'


def prepare_soap_from_url_list():
    with codecs.open('D:/data/sklt/sklt-res-hidden-url-html.txt', "r", "utf-8") as hidden_list:
        soup = BeautifulSoup(hidden_list, "html.parser")
        a_list = soup.select('a')
        print 'got a list'
        print len(a_list)
        my_dict = dict()
        idx = 0
        for a_line in a_list:
            idx += 1
            txt_items = a_line.string.split('#')
            # print a_line['href']
            if len(txt_items) > 1:
                my_dict[txt_items[1].strip()] = a_line
                # if idx > 2:
                #     break
        # print my_dict
        # for item in my_dict.items():
        #     print item[1]
        #     asoap = BeautifulSoup(str(item[1]), "html.parser")
        #     print asoap.a['href']
        #     print asoap.a['hidden_or_deleted']
        print len(my_dict)
        return my_dict


def compare_count():
    url_list = set()
    with codecs.open('D:/data/sklt/index-old-include-hidden.html', "r", "utf-8") as hidden_list:
        soup = BeautifulSoup(hidden_list, "html.parser")
        ul_list = soup.select_one("#js_content").select("a[hidden_or_deleted=manual]")
        print len(ul_list)
        for line in ul_list:
            url = line['href']
            if len(url) > 0:
                url_list.add(get_page_sn(url))
    print len(url_list)
    with codecs.open('D:/data/sklt/sklt-res-hidden-url-html.txt', "r", "utf-8") as hidden_list:
        soup = BeautifulSoup(hidden_list, "html.parser")
        a_list = soup.select('a')
        print len(a_list)
        for line in a_list:
            url = line['href']
            if get_page_sn(url) not in url_list:
                print line.string


def update_index_to_local_link(idx_page, save_page):
    page_path = tmp_dir + idx_page
    with codecs.open(page_path, "r", "utf-8") as html_page:
        soup = BeautifulSoup(html_page, "html.parser", from_encoding="utf-8")
        # print(soup.title.string.strip())

        link_list = soup.select_one("#js_content").select("a[href^=http]")
        print 'got link_list: %s ' % len(link_list)
        idx = 0
        for link in link_list:
            idx += 1
            # if idx > 10:
            #     break
            # print link
            sub_link = link['href']
            sub_sn = get_page_sn(sub_link)
            prefix = './sklt-res/'
            if link.has_attr('hidden_or_deleted'):
                prefix = './sklt-res-hidden/'
            local_link = prefix + sub_sn + '.html'
            link['href'] = local_link

            # print link

        # html_page.seek(0)
        # html_page.write(soup.prettify(formatter="html"))
        # html_page.truncate()
        with codecs.open(tmp_dir + save_page, "w", "utf-8") as temp:
            temp.write(soup.prettify(formatter="html"))
        print 'updated %s index to local refer' % len(link_list)


if __name__ == '__main__':
    # base_url = 'https://mp.weixin.qq.com/s?__biz=MzAxNTMxMTc0MA==&mid=205315770&idx=1&sn=8556c606ff340f29a598184580326bc5&scene=21#wechat_redirect'
    # base_url = 'http://mp.weixin.qq.com/s?__biz=MzAxNTMxMTc0MA==&mid=205864469&idx=1&sn=0b04583f8b94361c7a52f260bb7ccae1&scene=21#wechat_redirect'
    # sn in link
    # page_sn = get_page_sn(base_url)
    # base_url = 'https://mp.weixin.qq.com/s/n1jg9GAcy38qp2vAnmH0xA'
    base_url = 'https://mp.weixin.qq.com/s?__biz=MzAxNTMxMTc0MA==&mid=402554105&idx=1&sn=28eddaecc3d580b3def6dee5f6f46dd8&scene=20&pass_ticket=0LnIlaWYENT3Tze5juCdwAnUCzFahoz0fCQLiHpxwSDWUVmPy51kIGBhFa0mXiED#rd'
    # page = download_file(base_url)

    # if not os.path.isfile(tmp_dir + page):
    #     print 'download file fail, retry one'
    #     page = download_file()
    # page = 'b33795f303ee3230f8a5888903e562c7.html'
    # parse_page_local(page, page_sn)
    # replace_page_images(page)

    idx_page = 'index-old-include-hidden.html'
    # parse_index(idx_page)
    # download_from_url_list()
    # update_index('index-old-include-hidden.html')
    # prepare_soap_from_url_list()
    # compare_count()
    save_page = 'index-old-include-hidden-local-gen.html'
    update_index_to_local_link(idx_page, save_page)

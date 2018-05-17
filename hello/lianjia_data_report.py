import codecs
import cookielib
import urllib2
import time

from bs4 import BeautifulSoup

tmp_dir = 'D:/data/lianjia/dafeng/'

base_url = 'https://cd.lianjia.com/chengjiao/dafeng/'


# page = 'pg1'


def download_file(idx):
    print 'start download file'
    page = 'pg' + idx
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    resp = opener.open(base_url + page)
    print resp.headers['content-type']
    the_page = resp.read()
    html = unicode(the_page, 'utf-8')  # .encode('utf-8')
    # print html
    # with open(tmp_dir + "forum-97-4.html", "w") as pom_file:
    #     pom_file.write(html)
    with codecs.open(tmp_dir + page + ".html", "w", "utf-8") as temp:
        temp.write(html)


def get_parsed_line(hs):
    line = []
    cj = hs.select_one('div.info')
    # # print cj.get_text()
    title = cj.select_one('div.title').get_text().split(' ')
    xiaoqu = title[0]
    line.append(xiaoqu)
    # print xiaoqu
    huxing = title[1]
    line.append(huxing)
    # print huxing
    mianji = title[2].partition(u'\u5e73\u7c73')[0]
    # print mianji
    line.append(mianji)

    house_info = cj.select_one('div.houseInfo').get_text().partition('|')
    chaoxiang = house_info[0].strip()
    # print chaoxiang
    line.append(chaoxiang)
    hs_info = house_info[2].strip().replace('|', '-')
    # print hs_info
    line.append(hs_info)

    cj_date = cj.select_one('div.dealDate').get_text()
    # print cj_date
    line.append(cj_date)
    total_price = cj.select_one('div.totalPrice span').get_text()
    # print total_price
    line.append(total_price)

    louceng = cj.select_one('div.positionInfo').get_text()
    # print louceng
    line.append(louceng)
    unit_price = cj.select_one('div.unitPrice span').get_text()
    # print unit_price
    line.append(unit_price)

    guapai = cj.select_one('div.dealCycleeInfo span.dealCycleTxt span:nth-of-type(1)').get_text()
    # print guapai
    st = guapai.index(u'\u724c') + 1
    ed = guapai.index(u'\u4e07')
    guapai_price = guapai[st:ed]
    # print guapai_price
    line.append(guapai_price)

    gp_cj_gap = float(guapai_price) - float(total_price)
    line.append(str(gp_cj_gap))

    cj_cycle = 'na'
    cj_zq_item = cj.select_one('div.dealCycleeInfo span.dealCycleTxt span:nth-of-type(2)')
    if (cj_zq_item != None):
        cj_zhouqi = cj_zq_item.get_text()
        # print cj_zhouqi
        st = cj_zhouqi.index(u'\u671f') + 1
        ed = cj_zhouqi.index(u'\u5929')
        cj_cycle = cj_zhouqi[st:ed]
    # print cj_cycle
    line.append(cj_cycle)

    # print ','.join(line)
    return line


if __name__ == '__main__':
    download_file("1")
    exit(0)

    out_file = tmp_dir + "lj_cj_data-dafeng.csv"
    with codecs.open(out_file, "a", "utf-8") as f:
        for i in range(1, 2):
            time.sleep(1)
            print '#### processing pg' + str(i)
            download_file(str(i))
            print 'page saved'

            # list page
            page = 'pg' + str(i)
            page_path = tmp_dir + page + ".html"

            html_page = open(page_path, 'r')
            # print html_page
            soup = BeautifulSoup(html_page, "html.parser")
            # print(soup.title.string)

            house_list = soup.select('ul.listContent li')
            print len(house_list)

            # hs = house_list[0]
            # get_parsed_line(hs)

            for hs in house_list:
                line = get_parsed_line(hs)
                # print ','.join(line)
                f.write(','.join(line))
                f.write('\r\n')
                # break
    print 'end'

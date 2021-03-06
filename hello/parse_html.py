import codecs
import re

from bs4 import BeautifulSoup


def parse(soup, out_file):
    pm_list = soup.select('div.pm_statistics')
    if len(pm_list) != 2:
        print 'data source format changed, exit...'
        exit(1)
    ret_lines = []
    pm_sum = pm_list[0]
    title = pm_sum.select_one('div.pm_title > div.pm_titleright').get_text().strip()
    # print title
    ret_lines.append(title)

    header = ''
    for hd in pm_sum.select('div > table thead td'):
        header += hd.get_text().strip() + ','
    # print header[:-1]
    ret_lines.append(header)

    sum_line = pm_sum.select('div > table tbody tr')[0]
    summary = ''
    for hd in sum_line.select('td'):
        summary += hd.get_text().replace(',', '').strip() + ','
    # print summary

    ret_lines.append(summary)
    mark_value = sum_line.select_one('td:nth-of-type(6)').get_text().replace(',', '').strip()
    total_cash = sum_line.select_one('td:nth-of-type(10)').get_text().replace(',', '').strip()
    total_value = float(mark_value) + float(total_cash)
    print total_value

    detail = pm_list[1]
    q_header = ''
    for hd in detail.select('thead td'):
        q_header += hd.get_text().strip() + ','
    # print q_header
    ret_lines.append(q_header)

    qudao_list = detail.select('tbody tr')
    for hd in qudao_list:
        item_list = hd.select('td')
        item_line = ''
        for item in item_list:
            item_line += item.get_text().replace(',', '').strip() + ','
        # print item_line
        ret_lines.append(item_line)

    print '================'
    # for line in ret_lines:
    #     print line

    print
    date_str = pm_sum.select_one('div.pm_title > div.pm_titleright').get_text().strip()
    date_value = re.search(r'\d{4}-\d{2}-\d{2}', date_str).group()
    one_line = date_value + ','
    for hd in qudao_list:
        one_line += hd.select_one('td:nth-of-type(13)').get_text().replace(',', '').strip() + ','
    # print one_line[:-1]

    # calc percentage
    one_line += 'percent,'
    for hd in qudao_list:
        sub_sum = hd.select_one('td:nth-of-type(6)').get_text().replace(',', '').strip()
        p = float(sub_sum) / total_value * 100
        one_line += "{0:.1f}".format(p) + ','
    # print one_line[:-1]

    # calc market value
    one_line += 'mktval,'
    for hd in qudao_list:
        one_line += hd.select_one('td:nth-of-type(6)').get_text().replace(',', '').strip() + ','
    # print one_line[:-1]
    one_line += str(total_value) + ','
    print one_line[:-1]

    print 'start append one line to file %s' % out_file
    with codecs.open(out_file, "a", "utf-8") as outf:
        outf.write(one_line[:-1])
        outf.write('\r\n')
    print 'complete append'


if __name__ == '__main__':
    save_page = 'holding-20301_2018-05-17.html'
    data_dir = 'D:/data/ms-p-203_html/'

    out_file = data_dir + save_page
    with codecs.open(out_file, "r", "utf-8") as f:
        html = f.read()
        # html = unicode(html, 'gbk')
        soup = BeautifulSoup(html, "html.parser")
        parse(soup, data_dir + 'ms-p-203_report.csv')

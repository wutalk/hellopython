import re

from bs4 import BeautifulSoup

f = open('D:/wutalk/Nutstore/ms-p-203.html', 'r')
html = f.read()
f.close()
# html = unicode(html, 'gbk')
soup = BeautifulSoup(html, "html.parser")


# print html

def parse(soup):
    pm_list = soup.select('div.pm_statistics')
    if len(pm_list) != 2:
        print 'data source format changed, exit...'
        exit(1)
    ret_lines = []
    pm_sum = pm_list[0]
    title = pm_sum.select_one('div.pm_title > div.pm_titleright').get_text()
    # print title
    ret_lines.append(title)

    header = ''
    for hd in pm_sum.select('div > table thead td'):
        header += hd.get_text() + ','
    # print header[:-1]
    ret_lines.append(header)

    sum_line = pm_sum.select('div > table tbody tr')[0]
    summary = ''
    for hd in sum_line.select('td'):
        summary += hd.get_text().replace(',', '') + ','
    # print summary
    ret_lines.append(summary)
    mark_value = sum_line.select_one('td:nth-of-type(6)').get_text().replace(',', '')
    total_cash = sum_line.select_one('td:nth-of-type(10)').get_text().replace(',', '')
    total_value = float(mark_value) + float(total_cash)
    print total_value

    detail = pm_list[1]
    q_header = ''
    for hd in detail.select('thead td'):
        q_header += hd.get_text() + ','
    # print q_header
    ret_lines.append(q_header)

    qudao_list = detail.select('tbody tr')
    for hd in qudao_list:
        item_list = hd.select('td')
        item_line = ''
        for item in item_list:
            item_line += item.get_text().replace(',', '') + ','
        # print item_line
        ret_lines.append(item_line)

    print '================'
    # for line in ret_lines:
    #     print line

    print
    date_str = pm_sum.select_one('div.pm_title > div.pm_titleright').get_text()
    date_value = re.search(r'\d{4}-\d{2}-\d{2}', date_str).group()
    one_line = date_value + ','
    for hd in qudao_list:
        one_line += hd.select_one('td:nth-of-type(13)').get_text().replace(',', '') + ','
    # print one_line[:-1]

    # calc percentage
    one_line += 'percent,'
    for hd in qudao_list:
        sub_sum = hd.select_one('td:nth-of-type(6)').get_text().replace(',', '')
        p = float(sub_sum) / total_value * 100
        one_line += "{0:.1f}".format(p) + ','
    # print one_line[:-1]

    # calc market value
    one_line += 'mktval,'
    for hd in qudao_list:
        one_line += hd.select_one('td:nth-of-type(6)').get_text().replace(',', '') + ','
    print one_line[:-1]
    one_line += str(total_value) + ','

    print 'start append one line to file'
    f = open('D:/wutalk/security-privacy/ms-p-203_report.csv', 'a')
    f.write(one_line[:-1])
    f.write('\n')
    f.close()
    print 'complete append'

# parse(soup)

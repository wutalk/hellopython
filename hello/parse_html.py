import re

from bs4 import BeautifulSoup

f = open('E:/temp/ms-p-203.html', 'r')
html = f.read()
f.close()
# html = unicode(html, 'gbk')
soup = BeautifulSoup(html, "html.parser")
# print html

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

summary = ''
for hd in pm_sum.select('div > table tbody td'):
    summary += hd.get_text().replace(',', '') + ','
# print summary
ret_lines.append(summary)

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
for line in ret_lines:
    print line

print
date_str = pm_sum.select_one('div.pm_title > div.pm_titleright').get_text()
one_line = re.search(r'\d{4}-\d{2}-\d{2}', date_str).group() + ','
for hd in qudao_list:
    one_line += hd.select_one('td:nth-of-type(13)').get_text().replace(',', '') + ','
print one_line[:-1]

# f = open('E:/temp/ms-p-203_report.csv', 'a')
# f.write(one_line[:-1])
# f.write('\n')
# f.close()

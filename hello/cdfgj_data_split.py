import os.path

from bs4 import BeautifulSoup


def get_date_from_page_name(page):
    items = page.split('_')
    data_str = items[2]
    return data_str.split('.')[0]


def list_fgj_pages(data_dir):
    files = os.listdir(data_dir)
    fgj_pages = []
    for f in files:
        if f.startswith('cdfgj_cj') & f.endswith('.html'):
            fgj_pages.append(f)
    return fgj_pages


def parse_page(data_dir, page):
    page_path = data_dir + page
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
    for i in range(2, len(es_list) - 1):  # -1 means skip total
        line_item = es_list[i].select('td')
        # today = pd.datetime.today()
        # today = today.strftime('%Y-%m-%d')
        today = date_str
        line = [today, new_ershou]
        for j in range(len(line_item) - 1):
            # j+1 skip zhongxin chengqu
            line.append(line_item[j + 1].get_text().strip())
        # print ','.join(line)
        es_lines.append(','.join(line))
    return es_lines


if __name__ == '__main__':
    pages_dir = 'D:/data/cdfgj-data/'
    pages = list_fgj_pages(pages_dir)
    parse_page(pages_dir, pages[0])
